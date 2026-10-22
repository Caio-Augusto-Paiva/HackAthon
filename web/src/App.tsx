import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Inicio } from './paginas/Inicio';
import { Anamnese } from './paginas/Anamnese';

export function App() {
  return <BrowserRouter><Routes>
    <Route path="/" element={<Inicio />} />
    <Route path="/anamnese/:sessaoId" element={<Anamnese />} />
  </Routes></BrowserRouter>;
}
