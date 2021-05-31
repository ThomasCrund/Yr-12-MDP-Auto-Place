import React, { useState } from 'react'
import axios from 'axios'

export default function PlacementController() {
    const [ materialId, setMaterialId ] = useState("")
    const [ file, setFile ] = useState()

    let uploadFile = (e) => {
        setFile(e.target.files[0])
    }

    const runPlacement = (e) => {
        const form = new FormData();

        form.append("upload_file", file);

        axios.post(`/api/place/${materialId}`, form)
        .then(response => {
            console.log(response)
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
        </div>
    )
}
