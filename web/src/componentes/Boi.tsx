import grande from '../assets/boi-grande.svg';
import pergunta from '../assets/boi-pergunta.svg';
import parecer from '../assets/boi-parecer.svg';

const desenhos = { 360: grande, 132: pergunta, 96: parecer };

export function Boi({ tamanho = 132 }: { tamanho?: 360 | 132 | 96 }) {
  return <img src={desenhos[tamanho]} width={tamanho} height={tamanho} alt="" aria-hidden="true" />;
}
