import React, { useState } from 'react'
import { useOpenCv } from 'opencv-react'

function ImageUpload(props) {
    const { cv } = useOpenCv();
    const [ uploadedImgURL, setImage] = useState("");

    let onload = (e) => {
        console.log(e)
        let src = cv.imread(e.target);
        console.log(src.cols, src.rows)
        let dst = new cv.Mat();
        let dsize = new cv.Size(300, src.rows * 300 / src.cols);
        cv.resize(src, dst, dsize, 0, 0, cv.INTER_AREA);
        src.delete();
        console.log(dst, dst.isContinuous())
        props.onUpload(dst)
    }

    let uploadFile = (e) => {
        setImage(URL.createObjectURL(e.target.files[0]));
    }

    return (
        <div>
            <img id="imageSrc" alt="Nothing Uploaded" src={uploadedImgURL} onLoad={onload} style={{"display": "none"}} />
            <div className="caption">imageSrc <input type="file" id="fileInput" onChange={uploadFile} name="filex" /></div>    
        </div>
    )
}

export default ImageUpload
