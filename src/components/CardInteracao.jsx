import { formatarData } from '../utils/formatar.js'

export default function CardInteracao({ interacao }) {
  return (
    <article className="linha linha-interacao">
      <div>
        <p className="linha-kicker">Comando simulado</p>
        <p className="linha-titulo">{interacao.texto}</p>
        <p className="linha-meta">{formatarData(interacao.data)}</p>
      </div>
      <p className="linha-resposta">{interacao.resposta}</p>
    </article>
  )
}