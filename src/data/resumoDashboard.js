// Recorte simulado de outubro. Não é a contagem dos quatro trechos da consulta.
// Os três gráficos leem estes objetos. Se o grupo mudar um número, muda o desenho.
//
// Ponto de extensão: copiem um objeto para cada gráfico novo e documentem
// no README de onde saiu o número. Não encham este arquivo de campos soltos.

export const ocorrenciasPorTipo = {
  titulo: 'Ocorrências por tipo',
  labels: ['Vegetação', 'Buraco', 'Sinalização', 'Drenagem'],
  valores: [8, 5, 3, 2],
}

export const ocorrenciasPorRodovia = {
  titulo: 'Ocorrências por rodovia',
  labels: ['SP-280', 'SP-270', 'SP-021'],
  valores: [11, 4, 3],
}

export const velocimetros = [
  {
    id: 'atencao',
    titulo: 'Índice de atenção',
    valor: 72,
    maximo: 100,
    detalhe: 'quanto do mês pediu vistoria',
    cor: '#9a4e12',
  },
  {
    id: 'inspecao',
    titulo: 'Cobertura da inspeção',
    valor: 54,
    maximo: 100,
    detalhe: 'km previstos já percorridos',
    cor: '#1e3a5f',
  },
  {
    id: 'criticos',
    titulo: 'Trechos críticos',
    valor: 2,
    maximo: 8,
    detalhe: 'de 8 trechos acompanhados',
    cor: '#1e3a5f',
  },
]