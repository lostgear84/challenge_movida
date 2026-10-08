import PainelGraficos from '../components/PainelGraficos.jsx'

export default function Dashboard() {
  // Ponto de extensão: o gráfico novo do grupo entra em PainelGraficos,
  // com outro objeto em src/data/resumoDashboard.js. Documentem a escolha no README.
  return (
    <section>
      <h2>Dashboard</h2>
      <p className="intro">
        Barras, pizza e velocímetros do recorte simulado. A tela inicial já
        mostra este painel junto com a leitura rápida. Aqui ele fica isolado
        para o grupo ajustar só os gráficos.
      </p>
      <PainelGraficos />
    </section>
  )
}