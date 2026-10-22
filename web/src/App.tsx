import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Inicio } from './paginas/Inicio';

export function App() {
  return <BrowserRouter><Routes>
    <Route path="/" element={<Inicio />} />
    <Route path="/anamnese/:sessaoId" element={<p role="status">Carregando verificação…</p>} />
  </Routes></BrowserRouter>;
}
