import Header from './Header.jsx'
import Nav from './Nav.jsx'
import { plataforma } from '../data/plataforma.js'

export default function Layout({ children, paginaAtual, onNavegar }) {
  return (
    <div className="casca">
      <header className="topo">
        <div className="faixa">
          <Header
            marca={plataforma.marca}
            complemento={plataforma.complemento}
            curso={plataforma.curso}
          />
          <Nav paginaAtual={paginaAtual} onNavegar={onNavegar} />
        </div>
      </header>
      <main className="miolo">{children}</main>
    </div>
  )
}