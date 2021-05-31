import React, { useEffect, useState, useRef } from 'react'
import { useOpenCv } from 'opencv-react'


export default function MaskCreator(props) {
    const [ colours, setColours] = useState([]);
    const [ blur, setBlur] = useState(0);
    const [ bwMode, setBW ] = useState(false);
    const [ testColour, setTestColours] = useState([255, 255, 255])
    const { cv } = useOpenCv();
    // const maskGlobal = useRef(null);
    
    // const applyButtonCall = () => { 
    //     // console.log("buttonPressed", maskGlobal.current)
    //     props.onMaskChange(maskGlobal.current) 
    // }
    const range = 20

    useEffect(() => {
        if (cv) {
            let Img = new cv.Mat()
            let ksize = new cv.Size(blur, blur);
            if (blur !== 0) {
                cv.medianBlur(props.img, Img, 1 + Math.round(blur / 2) * 2 );
            } else {
                Img = props.img;
            }
            // cv.imshow('canvasOutput', props.img);
            cv.imshow('canvasBlurred', Img);
            // console.log(bwMode)
            let mask = cv.Mat.zeros(props.img.rows, props.img.cols, 0)
            for (let i = 0; i < colours.length; i++) {
                const element = colours[i];
                let dst = new cv.Mat()
                let low = new cv.Mat(props.img.rows, props.img.cols, props.img.type(), [element[0]-range, element[1]-range, element[2]-range, 0]);
                let high = new cv.Mat(props.img.rows, props.img.cols, props.img.type(), [element[0]+range, element[1]+range, element[2]+range, 255]);
                cv.inRange(Img, low, high, dst);
                cv.add(mask, dst, mask);
                low.delete();
                high.delete();
                dst.delete()
            }
            if (bwMode) {
                // let outputMapNotSelected = new cv.Mat(props.img.rows, props.img.cols, 0, new cv.Scalar(98, 163, 136))
                // let outputMapSelected = new cv.Mat(props.img.rows, props.img.cols, 0, new cv.Scalar(185, 210, 210))

            } else {
                cv.imshow('canvasMask', mask);
            }
            // maskGlobal.current = mask;
            if (colours.length !== 0) {
                props.onMaskChange(mask);
            }
            // Img.delete();
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [cv, props.img, colours, blur, bwMode])

    let canvasClick = (e) => {
        // console.log(props.img)
        let Img = new cv.Mat()
        if (blur !== 0) {
            cv.medianBlur(props.img, Img, 1 + Math.round(blur / 2) * 2 );
        } else {
            Img = props.img;
        }
        let xPos = e.clientX - e.target.offsetLeft
        let yPos = e.clientY - e.target.offsetTop
        let B = Img.data[yPos * props.img.cols * props.img.channels() + xPos * props.img.channels() + 2];
        let G = Img.data[yPos * props.img.cols * props.img.channels() + xPos * props.img.channels() + 1];
        let R = Img.data[yPos * props.img.cols * props.img.channels() + xPos * props.img.channels()];
        setColours(arrayExisting => {
            let found = false
            for (let i = 0; i < arrayExisting.length; i++) {
                found = (arrayExisting[i][0] === R && arrayExisting[i][1] === G && arrayExisting[i][2] === B) ? true : found
            }
            // console.log(found)
            if ( !found ) {
                return [[R, G, B], ...arrayExisting ]
            }
            
            return arrayExisting
        })

    }

    let canvasHover = (e) => {
        let Img = new cv.Mat()
        if (blur !== 0) {
            cv.medianBlur(props.img, Img, 1 + Math.round(blur / 2) * 2 );
        } else {
            Img = props.img;
        }
        let xPos = e.clientX - e.target.offsetLeft
        let yPos = e.clientY - e.target.offsetTop
        let B = Img.data[yPos * props.img.cols * props.img.channels() + xPos * props.img.channels() + 2];
        let G = Img.data[yPos * props.img.cols * props.img.channels() + xPos * props.img.channels() + 1];
        let R = Img.data[yPos * props.img.cols * props.img.channels() + xPos * props.img.channels()];
        setTestColours([R, G, B])
    }
    

    const styles ={
        padding: '10px',
        backgroundColor: '#B9D2D2',
        marginRight: "10px",
        borderRadius: 10,
    }

    return (
        <div style={{ 
            display: "flex",

        }}>
            <div style={{
                ...styles,
                display: 'flex',
                flexDirection: 'column',
            }}>
                <div>Blur: <input type="range" min={0} max={9} value={blur} onChange={e => setBlur(parseInt(e.target.value))} /> {blur}</div>
                {/* <div>MonoTone: <input type="checkbox" value={!bwMode} onChange={e => setBW(value => !value) } /></div> */}
                <div style={{ width: "21.5px", height: "21.5px", backgroundColor: `rgb(${testColour[0]}, ${testColour[1]}, ${testColour[2]})`}}></div>
            </div>
            <canvas style={{...styles, cursor: "crosshair" }} id="canvasBlurred" onClick={canvasClick} onMouseMoveCapture={canvasHover}></canvas>
            <canvas style={{...styles, cursor: "crosshair" }} id="canvasMask" onClick={canvasClick} onMouseMoveCapture={canvasHover}></canvas>
            <div  style={{
                ...styles,
                display: 'flex',
                flexDirection: 'column',
            }}>
                <span>Colour Selections</span>
                <div>{colours.map((value, index) => (
                    <div key={index} style={{display:"flex"}} onClick={() => {
                        // console.log("clicked", index, value)
                        setColours(colours.filter((value, indexCheck) => index !== indexCheck))
                    }}>
                        <div style={{ width: "21.5px", height: "21.5px", backgroundColor: `rgb(${value[0]}, ${value[1]}, ${value[2]})`}}></div>
                        <span>{`${value[0]}, ${value[1]}, ${value[2]}`}</span>
                    </div>
                ))}</div>
            </div>
        </div>
    )
}
