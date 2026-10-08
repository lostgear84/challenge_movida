import CardInteracao from '../components/CardInteracao.jsx'

export default function Interacoes({ interacoes }) {
  return (
    <section>
      <h2>Interações</h2>
      <p className="intro">
        Histórico simulado do que o operador teria dito ao agente de voz. Cada
        item mostra o comando, a data e uma resposta fixa.
      </p>

      {interacoes.length === 0 ? (
        <p className="vazio">Nenhuma interação simulada.</p>
      ) : (
        <ul className="lista">
          {interacoes.map((interacao) => (
            <li key={interacao.id}>
              <CardInteracao interacao={interacao} />
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}