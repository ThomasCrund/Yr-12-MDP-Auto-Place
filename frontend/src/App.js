import './App.css';
import MaterialImporter from './component/MaterialImporter'
import { OpenCvProvider } from 'opencv-react'
import PlacementController from './component/PlacementController';
import { useState } from 'react'
import NavBar from './component/NavBar';

function App() {
  const [ currentTab, setTab ] = useState(0)
  const [ openCVLoaded, setCV ] = useState(false)

  let onLoaded = (cv) => {
    setCV(true)
    console.log('opencv loaded, cv')
  }

  return (
    <div className="App">
      <NavBar tabClick={setTab} tab={currentTab} />
      <OpenCvProvider onLoad={onLoaded} >
        <div className="bodyWrapper">
          {openCVLoaded ? 
            currentTab === 0    ? <MaterialImporter />
                                : <PlacementController />
                         : "Waiting for OpenCV to Load"
          }
          
        </div>
      </OpenCvProvider>
      
    </div>
  );
}

export default App;
