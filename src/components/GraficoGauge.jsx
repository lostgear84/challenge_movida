import { Doughnut } from 'react-chartjs-2'
import { registrarCharts } from '../utils/charts.js'

registrarCharts()

// Velocímetro: meia rosca. valor / maximo preenche o arco.
// Ponto de extensão: cada índice novo é um objeto em velocimetros,
// não um gráfico desenhado na mão dentro daqui.
export default function GraficoGauge({
  titulo,
  valor,
  maximo,
  detalhe,
  cor = '#1e3a5f',
}) {
  const resto = Math.max(maximo - valor, 0)

  const dados = {
    datasets: [
      {
        data: [valor, resto],
        backgroundColor: [cor, '#e4e7ec'],
        borderWidth: 0,
      },
    ],
  }

  const opcoes = {
    responsive: true,
    maintainAspectRatio: false,
    rotation: -90,
    circumference: 180,
    cutout: '76%',
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false },
    },
  }

  return (
    <figure className="gauge">
      <div className="gauge-arco">
        <Doughnut data={dados} options={opcoes} />
        <p className="gauge-valor">
          {valor}
          <span>/{maximo}</span>
        </p>
      </div>
      <figcaption>
        <strong>{titulo}</strong>
        <span>{detalhe}</span>
      </figcaption>
    </figure>
  )
}