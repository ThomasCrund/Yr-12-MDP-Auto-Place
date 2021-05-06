import React, { useEffect, useState } from 'react'
import { useOpenCv } from 'opencv-react'

export default function CutoutFinder(props) {
    const [ minArea, setMinArea ] = useState(0);
    const { cv } = useOpenCv();

    console.log("CutoutFinder", props)

    useEffect(() => {

        let dst = cv.Mat.zeros(props.mask.rows, props.mask.cols, cv.CV_8UC3);
        let dstApprox = cv.Mat.zeros(props.mask.rows, props.mask.cols, cv.CV_8UC3);

        let contours = new cv.MatVector();
        let hierarchy = new cv.Mat();

        cv.findContours(props.mask, contours, hierarchy, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE);
        
        // array to store contours once they have been cleaned up
        let poly = new cv.MatVector();

        // draw contours with random Scalar
        for (let i = 0; i < contours.size(); ++i) {


            let color = new cv.Scalar(Math.round(Math.random() * 255), Math.round(Math.random() * 255),
                                    Math.round(Math.random() * 255));

            cv.drawContours(dst, contours, i, color, 1, cv.LINE_8, hierarchy, 100);

            let cleanedCnt = new cv.Mat();
            let cnt = contours.get(i);
            
            //Approximate the contour to clean up the edges.
            cv.approxPolyDP(cnt, cleanedCnt, 1, true);
            poly.push_back(cleanedCnt);

            //Only output if area is greater than threshold
            let area = cv.contourArea(cleanedCnt, false);
            if (area > minArea) {
                cv.drawContours(dstApprox, poly, i, color, 1);
            }

            cnt.delete(); cleanedCnt.delete();
        }

        //Update Output Frames
        cv.imshow('canvasContours', dst);
        cv.imshow('canvasApprox', dstApprox);

        dst.delete(); contours.delete(); hierarchy.delete();

    }, [cv, props.mask, minArea])

    let saveClick = () => {

        //// I recalculate everything due to issues i was having saving contours in state.

        //Setup mats for contours and hierarchy(not used)
        let contours = new cv.MatVector();
        let hierarchy = new cv.Mat();

        cv.findContours(props.mask, contours, hierarchy, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE);

        //Approximate the contour to clean up the edges.
        for (let i = 0; i < contours.size(); ++i) {
            
            let cnt = contours.get(i);
            let cleanedCnt = new cv.Mat();
            
            //Approximate the contour to clean up the edges.
            cv.approxPolyDP(cnt, cleanedCnt, 1, true);

            //Only output if area is greater than threshold
            let area = cv.contourArea(cleanedCnt, false);
            if (area > minArea) {

                console.log(area, cleanedCnt.data, cleanedCnt.data.length)
            }
            

            cleanedCnt.delete();
            cnt.delete(); 
        }

        contours.delete(); hierarchy.delete();
    }


    return (
        <div>
            <div>
                Min Contour Area: <input type="range" min={0} max={200} value={minArea} onChange={e => setMinArea(parseInt(e.target.value))} /> {minArea}
            </div>
            <canvas id="canvasContours" ></canvas>
            <canvas id="canvasApprox" ></canvas>
            <button onClick={saveClick}>Save Contours</button>
        </div>
    )
}
