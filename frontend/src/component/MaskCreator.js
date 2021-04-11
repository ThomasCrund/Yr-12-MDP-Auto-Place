import React, { useEffect, useState } from 'react'
import { useOpenCv } from 'opencv-react'


export default function MaskCreator(props) {
    const [ colours, setColours] = useState([]);
    const [ blur, setBlur] = useState(0);
    const { cv } = useOpenCv();

    useEffect(() => {
        if (cv) {
            let Img = new cv.Mat()
            let ksize = new cv.Size(blur, blur);
            if (blur !== 0) {
                // cv.blur(props.img, Img, ksize)
                // cv.GaussianBlur(props.img, Img, ksize, 0, 0, cv.BORDER_DEFAULT)
                // cv.GaussianBlur(props.img, Img, ksize, 0, 0, cv.BORDER_DEFAULT);
                cv.medianBlur(props.img, Img, 1 + Math.round(blur / 2) * 2 );
            } else {
                Img = props.img;
            }
            // cv.imshow('canvasOutput', props.img);
            cv.imshow('canvasBlurred', Img);
            let mask = cv.Mat.zeros(props.img.rows, props.img.cols, 0);
            for (let i = 0; i < colours.length; i++) {
                const element = colours[i];
                let dst = new cv.Mat()
                let low = new cv.Mat(props.img.rows, props.img.cols, props.img.type(), [element[0]-10, element[1]-10, element[2]-10, 0]);
                let high = new cv.Mat(props.img.rows, props.img.cols, props.img.type(), [element[0]+10, element[1]+10, element[2]+10, 255]);
                cv.inRange(Img, low, high, dst);
                cv.add(mask, dst, mask);
                low.delete();
                high.delete();
                dst.delete()
            }
            cv.imshow('canvasMask', mask);
            // Img.delete();
        }
    }, [cv, props.img, colours, blur])

    let canvasClick = (e) => {
        // console.log(props.img)
        let xPos = e.clientX - e.target.offsetLeft
        let yPos = e.clientY - e.target.offsetTop
        let B = props.img.data[yPos * props.img.cols * props.img.channels() + xPos * props.img.channels() + 2];
        let G = props.img.data[yPos * props.img.cols * props.img.channels() + xPos * props.img.channels() + 1];
        let R = props.img.data[yPos * props.img.cols * props.img.channels() + xPos * props.img.channels()];
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
    
    



    return (
        <div>
            <div>
                Blur: <input type="range" min={0} max={9} value={blur} onChange={e => setBlur(parseInt(e.target.value))} /> {blur}
            </div>
            {/* <canvas id="canvasOutput" onClick={canvasClick} ></canvas> */}
            <canvas id="canvasBlurred" onClick={canvasClick} ></canvas>
            <div>{JSON.stringify(colours, 2)}</div>
            <canvas id="canvasMask" onClick={canvasClick} ></canvas>
        </div>
    )
}
