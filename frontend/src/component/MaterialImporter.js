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
    const [ tab, setTab ] = useState(0)

    let uploadHandler = (fileMat) => {
        setImg(fileMat)
        setTab(1)
        console.log(img)
    }

    let maskHandler = (newMask) => {
        setMask(newMask)
    }

    let getNavStyle = (tabNum) => {
        return {
            padding: (60 - 21.25)/2,
            borderRight: "1px solid #055E68",
            cursor: "Pointer",
            backgroundColor: tabNum === tab ? "#055E68" : "transparent",
            color: tabNum === tab ? "white" : "#055E68",
        }
    }

    return (
        <div className="displayArea">
            <div style={{
                display: "flex",
                height: "60px"
            }}>
                <div style={getNavStyle(0)} onClick={() => setTab(0)}><span>Upload</span></div>
                <div style={getNavStyle(1)} onClick={() => setTab(img !== undefined ? 1 : 0)}><span>Mask</span></div>
                <div style={getNavStyle(2)} onClick={() => setTab(mask !== undefined ? 2 :(img !== undefined ? 1 : 0))}><span>Generate</span></div>
            </div>
            <div style={{width: "100%", borderBottom: "1px solid #2C2C2C", margin: "10px 0"}} ></div>
            {tab === 0
            ? <ImageUpload onUpload={uploadHandler} />
            : null}
            {img !== undefined && tab === 1
            ? <MaskCreator img={img} onMaskChange={maskHandler}/>
            : null}
            {mask !== undefined && tab === 2
            ? <CutoutFinder mask={mask} />
            : null}
            
            <div></div>
        </div>
    )
}
