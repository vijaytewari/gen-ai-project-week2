import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/base.css';
import './styles/shell.css';
import './styles/library.css';
import './styles/review.css';
import './styles/assistant.css';
import './styles/reports.css';
import './styles/ocr.css';
import './styles/json.css';
import './styles/saved-library.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode><App /></React.StrictMode>,
);
