import React, { useState } from 'react'
// import { useOpenCv } from 'opencv-react'
import ImageUpload from './ImageUpload'
import MaskCreator from './MaskCreator'

export default function MaterialImporter() {
    // const { cv } = useOpenCv()
    // const [ colours, setColours] = useState([]);
    const [ img, setImg ] = useState()

    let uploadHandler = (fileMat) => {
        setImg(fileMat)
        console.log(img)
    }

    return (
        <div>
            <ImageUpload onUpload={uploadHandler} />
            {img !== undefined 
            ? <MaskCreator img={img}/>
            : null}
            
            <div></div>
        </div>
    )
}
