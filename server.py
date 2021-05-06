from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles


async def materialPost(request):
    body = await request.json()

    return JSONResponse({'id': request.path_params['matId'], 'body': body})


async def materialGet(request):
    return JSONResponse({'id': request.path_params['matId']})


app = Starlette(debug=True, routes=[
    
    Mount('/api', routes=[
        # Route('/material', materialPost, methods=['GET']),
        Route('/material/{matId}', materialPost, methods=['POST']),
        Route('/material/{matId}', materialPost, methods=['GET'])
    ], name="api"),
    Mount('/', app=StaticFiles(directory='frontend/build', html=True)),
])