import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Inicio } from './paginas/Inicio';
import { Anamnese } from './paginas/Anamnese';
import { Parecer } from './paginas/Parecer';
import { Privacidade } from './paginas/Privacidade';

export function App() {
  return <BrowserRouter><Routes>
    <Route path="/" element={<Inicio />} />
    <Route path="/anamnese/:sessaoId" element={<Anamnese />} />
    <Route path="/parecer/:sessaoId" element={<Parecer />} />
    <Route path="/privacidade" element={<Privacidade />} />
  </Routes></BrowserRouter>;
}
