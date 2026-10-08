export default function Header({ marca, complemento, curso }) {
  return (
    <div className="marca-linha">
      <div className="marca">
        <span className="marca-icone" aria-hidden="true">
          MC
        </span>
        <div>
          <strong>{marca}</strong>
          <p className="marca-complemento">{complemento}</p>
        </div>
      </div>
      <p className="topo-curso">{curso}</p>
    </div>
  )
}