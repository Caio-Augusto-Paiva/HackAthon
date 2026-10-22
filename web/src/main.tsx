import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './estilo/global.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode><main aria-label="Anamnese Bovina" /></StrictMode>,
);
