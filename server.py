from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from filestorage import store
from filestorage.handlers import AsyncLocalFileHandler
import uvicorn

from Placement.util.methods.MatFromJSON import GenerateMaterialJSON
from Placement.util.methods.dxfImport import partFromDxf
from Placement.util.methods.place import placePerimeter

import cv2 as cv
import numpy as np
import json
import ezdxf
import time

async def materialPost(request):
    body = await request.json()
    print(body)

    dataString = json.dumps(body)

    with open(f"data/{request.path_params['matId']}.json", "w") as saveFile:
        saveFile.write(dataString)

    img = np.ones((body["height"], body["width"], 3), np.uint8)*255
    material = GenerateMaterialJSON(body)
    material.displayOnImage(img)
    cv.imwrite("OutputTesting/ServerTest.jpg", img)

    return JSONResponse({'id': request.path_params['matId'], 'success': True})


async def materialGet(request):
    return JSONResponse({'id': request.path_params['matId']})


async def runPlace(request):
    form = await request.form()
    filename = form["upload_file"].filename
    contents = await form["upload_file"].read()
    with open(f'data/{filename}', 'wb') as f:
        f.write(contents)
    f = open(f"data/{request.path_params['matId']}.json", "r")
    matJSON = json.loads(f.read())
    material = GenerateMaterialJSON(matJSON)
    part = partFromDxf(f'data/{filename}')

    startTime = time.time()

    result = placePerimeter(material, part)

    print("##!#", result)
    if result[0] != 0 and result[0] != 0 and result[0] != 0:

        return JSONResponse({"success":True, "time": time.time() - startTime, "result": {"x": result[0], "y": result[1], "rot": result[2] * 180 / 3.14159265359}})
    return JSONResponse({"success": False, "message": "Part did not fit on material"})

# async def some_startup_task():
#     print(store.handler)
    # await store.async_finalize_config()

app = Starlette(debug=True, routes=[
    
    Mount('/api', routes=[
        # Route('/material', materialPost, methods=['GET']),
        Route('/material/{matId}', materialPost, methods=['POST']),
        Route('/material/{matId}', materialPost, methods=['GET']),
        Route('/place/{matId}', runPlace, methods=['POST'])
    ], name="api"),
    Mount('/', app=StaticFiles(directory='frontend/build', html=True)),
])
# , on_startup=[some_startup_task]

if __name__ == "__main__":
    # store.handler = AsyncLocalFileHandler(
    #     base_path='/data', auto_make_dir=True,
    # )
    # store.finalize_config()
    # print(store.handler)
    

    uvicorn.run("server:app", host='0.0.0.0', port=8000, reload=True)