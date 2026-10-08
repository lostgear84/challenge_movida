import { formatarData } from '../utils/formatar.js'

export default function CardTrecho({ trecho }) {
  return (
    <article className="linha">
      <div>
        <p className="linha-titulo">
          {trecho.rodovia} · {trecho.nome}
        </p>
        <p className="linha-meta">
          km {trecho.kmInicial} ao km {trecho.kmFinal} · sentido {trecho.sentido}
        </p>
      </div>
      <p className={trecho.atencao ? 'linha-alerta' : 'linha-situacao'}>
        {trecho.situacao}
      </p>
      <p className="linha-meta">{formatarData(trecho.atualizadoEm)}</p>
    </article>
  )
}