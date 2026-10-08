import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Tooltip,
} from 'chart.js'

let registrado = false

export function registrarCharts() {
  if (registrado) return

  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    Tooltip,
    Legend,
  )

  ChartJS.defaults.font.family = "'Source Sans 3', 'Segoe UI', sans-serif"
  ChartJS.defaults.color = '#5c6773'
  ChartJS.defaults.borderColor = '#e1e5ea'

  registrado = true
}