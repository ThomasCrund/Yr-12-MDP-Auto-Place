import './App.css';
import MaterialImporter from './component/MaterialImporter'
import { OpenCvProvider } from 'opencv-react'
import PlacementController from './component/PlacementController';
import { useState } from 'react'
import NavBar from './component/NavBar';

function App() {
  const [ currentTab, setTab ] = useState(0)

  let onLoaded = (cv) => {
    console.log('opencv loaded, cv')
  }

  return (
    <div className="App">
      <NavBar tabClick={setTab} tab={currentTab} />
      <OpenCvProvider onLoad={onLoaded} >
        <div className="bodyWrapper">
          {currentTab === 0   ? <MaterialImporter />
                              : <PlacementController />
          }
        </div>
      </OpenCvProvider>
      
    </div>
  );
}

export default App;
