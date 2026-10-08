import { Pie } from 'react-chartjs-2'
import { registrarCharts } from '../utils/charts.js'

registrarCharts()

const CORES = ['#1e3a5f', '#9a4e12', '#6d7c8a', '#c5ccd4']

// Ponto de extensão: a pizza serve para uma parte de um todo
// (rodovia, turno, sentido). Troquem CORES se a paleta do grupo for outra.
export default function GraficoPizza({ titulo, labels, valores }) {
  const dados = {
    labels,
    datasets: [
      {
        data: valores,
        backgroundColor: labels.map((_, indice) => CORES[indice % CORES.length]),
        borderWidth: 0,
      },
    ],
  }

  const opcoes = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          boxWidth: 8,
          boxHeight: 8,
          padding: 14,
          color: '#3d4854',
        },
      },
    },
  }

  return (
    <figure className="grafico">
      <figcaption>{titulo}</figcaption>
      <div className="grafico-area">
        <Pie data={dados} options={opcoes} />
      </div>
    </figure>
  )
}