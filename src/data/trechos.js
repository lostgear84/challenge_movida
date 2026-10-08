// Dados fixos da Sprint 1. Números e situações são simulados para a aula.
// TODO Sprint 2: este array deixa de alimentar a tela direto.
// Ele vira o valor inicial do useState de trechos no App.jsx
// (ou a lista começa vazia e o grupo cadastra pelo formulário).
export const trechos = [
  {
    id: 't-sp280-40',
    rodovia: 'SP-280',
    nome: 'Castello Branco',
    kmInicial: 40,
    kmFinal: 48,
    sentido: 'interior',
    situacao: 'Vegetação alta na faixa de domínio',
    atencao: true,
    atualizadoEm: '2026-10-05T14:30:00',
  },
  {
    id: 't-sp280-61',
    rodovia: 'SP-280',
    nome: 'Castello Branco',
    kmInicial: 61,
    kmFinal: 70,
    sentido: 'capital',
    situacao: 'Buraco no acostamento',
    atencao: true,
    atualizadoEm: '2026-10-06T09:15:00',
  },
  {
    id: 't-sp270-18',
    rodovia: 'SP-270',
    nome: 'Raposo Tavares',
    kmInicial: 18,
    kmFinal: 25,
    sentido: 'interior',
    situacao: 'Placa de velocidade encoberta',
    atencao: false,
    atualizadoEm: '2026-10-04T16:05:00',
  },
  {
    id: 't-sp021-12',
    rodovia: 'SP-021',
    nome: 'Rodoanel',
    kmInicial: 12,
    kmFinal: 16,
    sentido: 'leste',
    situacao: 'Drenagem obstruída no acostamento',
    atencao: false,
    atualizadoEm: '2026-10-03T11:40:00',
  },
]