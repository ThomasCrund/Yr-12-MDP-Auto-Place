import './App.css';
import MaterialImporter from './component/MaterialImporter'
import { OpenCvProvider } from 'opencv-react'

function App() {

  let onLoaded = (cv) => {
    console.log('opencv loaded, cv')
  }

  return (
    <div className="App">
      <h1>Auto Place</h1>
      <OpenCvProvider onLoad={onLoaded} >
        <MaterialImporter />
      </OpenCvProvider>
      
    </div>
  );
}

export default App;
