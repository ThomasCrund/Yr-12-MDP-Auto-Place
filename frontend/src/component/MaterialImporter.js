import React, { useState } from 'react'
// import { useOpenCv } from 'opencv-react'
import ImageUpload from './ImageUpload'
import MaskCreator from './MaskCreator'
import CutoutFinder from './CutoutFinder'

export default function MaterialImporter() {
    // const { cv } = useOpenCv()
    // const [ colours, setColours] = useState([]);
    const [ img, setImg ] = useState()
    const [ mask, setMask ] = useState()

    let uploadHandler = (fileMat) => {
        setImg(fileMat)
        console.log(img)
    }

    let maskHandler = (newMask) => {
        setMask(newMask)
    }

    return (
        <div>
            <ImageUpload onUpload={uploadHandler} />
            {img !== undefined 
            ? <MaskCreator img={img} onMaskChange={maskHandler}/>
            : null}
            {mask !== undefined 
            ? <CutoutFinder mask={mask} />
            : null}
            
            <div></div>
        </div>
    )
}
