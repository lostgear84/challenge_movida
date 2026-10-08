export function formatarData(iso) {
  return new Date(iso).toLocaleString('pt-BR', {
    dateStyle: 'short',
    timeStyle: 'short',
  })
}

export function somar(valores) {
  let total = 0
  for (const valor of valores) {
    total += valor
  }
  return total
}

// TODO Sprint 2: criar src/utils/analisarTrecho.js, no espírito do
// analisarPerfil do CardioIA. A função recebe as ocorrências do trecho
// atual e devolve total, quantas são de gravidade alta, o tipo mais
// frequente e se cabe um alerta. Não implementem isso na Sprint 1.