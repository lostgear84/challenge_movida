import { Bar } from 'react-chartjs-2'
import { registrarCharts } from '../utils/charts.js'

registrarCharts()

// Ponto de extensão: outro gráfico de barras é outro uso deste componente,
// com outros labels e valores. Não coloquem um segundo <Bar> aqui dentro.
export default function GraficoBarras({
  titulo,
  labels,
  valores,
  cor = '#1e3a5f',
}) {
  const dados = {
    labels,
    datasets: [
      {
        label: 'Quantidade',
        data: valores,
        backgroundColor: cor,
        borderRadius: 2,
        maxBarThickness: 42,
      },
    ],
  }

  const opcoes = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { color: '#5c6773' },
      },
      y: {
        beginAtZero: true,
        ticks: { precision: 0, color: '#5c6773' },
        grid: { color: '#e6e8ec' },
        border: { display: false },
      },
    },
  }

  return (
    <figure className="grafico">
      <figcaption>{titulo}</figcaption>
      <div className="grafico-area">
        <Bar data={dados} options={opcoes} />
      </div>
    </figure>
  )
}