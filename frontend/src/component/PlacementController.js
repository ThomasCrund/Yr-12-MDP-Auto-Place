import React, { useState } from 'react'
import axios from 'axios'

export default function PlacementController() {
    const [ materialId, setMaterialId ] = useState("")
    const [ file, setFile ] = useState()
    const [ placementResult, setResult ] = useState({"Result": false})

    let uploadFile = (e) => {
        setFile(e.target.files[0])
    }

    const runPlacement = (e) => {
        const form = new FormData();

        form.append("upload_file", file);

        axios.post(`/api/place/${materialId}`, form)
        .then(response => {
            console.log(response)
            if (response.data.success) {
                setResult({
                    Result: true, 
                    success: true,
                    time: response.data.time,
                    position: response.data.result
                })
            } else {
                setResult({
                    Result: true, 
                    success: false,
                    message: response.data.message
                })
            }
        })
        .catch(err => {
            console.log(err)
        })
    }

    
    return (
        <div className="displayArea">
            Part File (dxf): <input type="file" name="Select DXF file" onChange={uploadFile} />
            Material Id: <input type="text" value={materialId} onChange={(e) => setMaterialId(e.target.value)} />
            <button onClick={runPlacement}>Run Placement</button>
            <br/>
            {placementResult.Result ? 
            <div>
                {placementResult.success ? 
                <div style={{backgroundColor: "#62A388", padding: "10px", borderRadius: "5px"}}>
                    <h4>Successful Placement</h4>
                    <div>
                        Time: {placementResult.time} seconds<br/>
                        <div>
                            <span>X: {placementResult.position.x}</span><br/>
                            <span>Y: {placementResult.position.y}</span><br/>
                            <span>Rot: {placementResult.position.rot}</span>
                        </div>
                    </div>
                    <img src="/placementOutput/OutputImage.jpg" alt="Could not find result"/>
                </div> : 
                <div style={{backgroundColor: "#F69393", padding: "10px", borderRadius: "5px"}}>
                    <h4>Did Not Place</h4>
                    <div>
                        {placementResult.message}
                    </div>
                </div>}
            </div>
            : null}
            Changed
        </div>
    )
}
