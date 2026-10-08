import PainelGraficos from '../components/PainelGraficos.jsx'
import TabelaTrechos from '../components/TabelaTrechos.jsx'
import { plataforma } from '../data/plataforma.js'
import { ocorrenciasPorTipo } from '../data/resumoDashboard.js'
import { somar } from '../utils/formatar.js'

export default function Home({ trechos, interacoes, onNavegar }) {
  const emAtencao = trechos.filter((trecho) => trecho.atencao).length
  const ocorrenciasMes = somar(ocorrenciasPorTipo.valores)

  return (
    <section className="painel">
      <div className="abertura">
        <p className="nota-exemplo">Exemplo de aula. Substituam pelo problema do grupo.</p>
        <h2>{plataforma.problemaTitulo}</h2>
        <p className="lead">{plataforma.problemaTexto}</p>
        <p className="meta">
          {plataforma.usuario}. {plataforma.resumo}
        </p>
        <p className="acoes">
          <button type="button" className="link-acao" onClick={() => onNavegar('consultas')}>
            Consultar trechos
          </button>
          <button
            type="button"
            className="link-acao secundario"
            onClick={() => onNavegar('interacoes')}
          >
            Ler interações
          </button>
        </p>
      </div>

      <dl className="indicadores">
        <div className="ind ind-navy">
          <dt>Trechos na malha</dt>
          <dd>{trechos.length}</dd>
        </div>
        <div className="ind ind-ambar">
          <dt>Em atenção</dt>
          <dd>{emAtencao}</dd>
        </div>
        <div className="ind ind-teal">
          <dt>Comandos simulados</dt>
          <dd>{interacoes.length}</dd>
        </div>
        <div className="ind ind-ceu">
          <dt>Ocorrências no recorte</dt>
          <dd>{ocorrenciasMes}</dd>
        </div>
      </dl>

      <PainelGraficos />
      <TabelaTrechos trechos={trechos} />
    </section>
  )
}