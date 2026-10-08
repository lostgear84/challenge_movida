import { formatarData } from '../utils/formatar.js'

export default function TabelaTrechos({ trechos }) {
  return (
    <div className="leitura">
      <h3>Leitura rápida dos trechos</h3>
      {trechos.length === 0 ? (
        <p className="vazio">Nenhum trecho para consultar.</p>
      ) : (
        <div className="tabela-rolagem">
          <table className="tabela">
            <thead>
              <tr>
                <th>Rodovia</th>
                <th>Trecho</th>
                <th>Sentido</th>
                <th>Situação</th>
                <th>Atualizado</th>
              </tr>
            </thead>
            <tbody>
              {trechos.map((trecho) => (
                <tr key={trecho.id}>
                  <td>
                    {trecho.rodovia}
                    <span className="tabela-nome">{trecho.nome}</span>
                  </td>
                  <td>
                    km {trecho.kmInicial} ao {trecho.kmFinal}
                  </td>
                  <td>{trecho.sentido}</td>
                  <td className={trecho.atencao ? 'celula-atencao' : undefined}>
                    {trecho.situacao}
                  </td>
                  <td>{formatarData(trecho.atualizadoEm)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}