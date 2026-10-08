import { useEffect, useState } from 'react'
import Layout from './components/Layout.jsx'
import Home from './pages/Home.jsx'
import Consultas from './pages/Consultas.jsx'
import Interacoes from './pages/Interacoes.jsx'
import Dashboard from './pages/Dashboard.jsx'
import { trechos as trechosFixos } from './data/trechos.js'
import { interacoes as interacoesFixas } from './data/interacoes.js'
import { plataforma } from './data/plataforma.js'
import './App.css'

export default function App() {
  const [pagina, setPagina] = useState('inicio')

  // TODO Sprint 2: os arrays fixos saem daqui e passam a viver no estado.
  // const [trechos, setTrechos] = useState(trechosFixos)
  // const [trechoAtualId, setTrechoAtualId] = useState(null)
  // const [ocorrencias, setOcorrencias] = useState([])
  // Um único objeto no localStorage, lido ao abrir e gravado a cada mudança.
  // F5 não pode apagar. Não implementem formulário, filtro, status nem
  // painel calculado na Sprint 1.
  const trechos = trechosFixos
  const interacoes = interacoesFixas

  useEffect(() => {
    const titulos = {
      inicio: plataforma.marca,
      consultas: `Consultas | ${plataforma.marca}`,
      interacoes: `Interações | ${plataforma.marca}`,
      dashboard: `Dashboard | ${plataforma.marca}`,
    }
    document.title = titulos[pagina] ?? plataforma.marca
  }, [pagina])

  return (
    <Layout paginaAtual={pagina} onNavegar={setPagina}>
      {pagina === 'inicio' && (
        <Home trechos={trechos} interacoes={interacoes} onNavegar={setPagina} />
      )}
      {pagina === 'consultas' && <Consultas trechos={trechos} />}
      {pagina === 'interacoes' && <Interacoes interacoes={interacoes} />}
      {pagina === 'dashboard' && <Dashboard />}
    </Layout>
  )
}