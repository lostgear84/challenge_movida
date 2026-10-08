// Histórico simulado. O agente de voz ainda não existe.
// Cada item é um comando que o operador teria falado, com data e resposta fixa.
export const interacoes = [
  {
    id: 'i-1',
    texto: 'Registrar vegetação alta no km 42',
    data: '2026-10-05T14:32:00',
    resposta:
      'Comando simulado recebido. Vegetação alta anotada no km 42 da SP-280, sentido interior. Nesta sprint a resposta é fixa: ninguém está ouvindo o microfone.',
  },
  {
    id: 'i-2',
    texto: 'Consultar a situação do km 65',
    data: '2026-10-06T09:18:00',
    resposta:
      'Trecho simulado da SP-280, km 61 ao 70, sentido capital. Situação registrada: buraco no acostamento.',
  },
  {
    id: 'i-3',
    texto: 'A placa do km 20 da Raposo está coberta pelo mato',
    data: '2026-10-04T16:12:00',
    resposta:
      'Comando simulado associado à SP-270, km 18 ao 25. Situação: placa de velocidade encoberta.',
  },
  {
    id: 'i-4',
    texto: 'Tem água empoçada no acostamento do km 14 do Rodoanel',
    data: '2026-10-03T11:48:00',
    resposta:
      'Comando simulado associado à SP-021, km 12 ao 16. Situação: drenagem obstruída no acostamento.',
  },
]