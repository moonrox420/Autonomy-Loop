import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// Create the root element and render the App. StrictMode is enabled
// to highlight potential problems in the development environment.
ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);