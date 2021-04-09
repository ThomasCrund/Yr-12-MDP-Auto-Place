import React, { useEffect, useState } from 'react'
import { useOpenCv } from 'opencv-react'

export default function MaskCreator(props) {
    const [ colours, setColours] = useState([]);
    const { cv } = useOpenCv();

    useEffect(() => {
        if (cv) {
            cv.imshow('canvasOutput', props.img);
            let mask = cv.Mat.zeros(props.img.rows, props.img.cols, 0);
            for (let i = 0; i < colours.length; i++) {
                const element = colours[i];
                let dst = new cv.Mat()
                let low = new cv.Mat(props.img.rows, props.img.cols, props.img.type(), [element[0]-10, element[1]-10, element[2]-10, 0]);
                let high = new cv.Mat(props.img.rows, props.img.cols, props.img.type(), [element[0]+10, element[1]+10, element[2]+10, 255]);
                cv.inRange(props.img, low, high, dst);
                cv.add(mask, dst, mask);
                low.delete();
                high.delete();
                dst.delete()
            }
            cv.imshow('canvasMask', mask);
            
        }
    }, [cv, props.img, colours])

    let canvasClick = (e) => {
        console.log(props.img)
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
            console.log(found)
            if ( !found ) {
                return [[R, G, B], ...arrayExisting ]
            }
            
            return arrayExisting
        })

    }
    
    



    return (
        <div>
            <canvas id="canvasOutput" onClick={canvasClick} ></canvas>
            <div>{JSON.stringify(colours, 2)}</div>
            <canvas id="canvasMask" onClick={canvasClick} ></canvas>
        </div>
    )
}
