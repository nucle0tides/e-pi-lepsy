import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  const [currMessage, setMessage] = useState("")

  useEffect(() => {
    fetch("/hi").then(res => res.json()).then(data => {
      setMessage(data.message)
    })
  })

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>useEffect: {currMessage}</p>
      </header>
    </div>
  );
}

export default App;