# sprint1-pln — Fundamentos da interação (Challenge Motiva–FIAP)

Camada de NLU do agente de voz: taxonomia de intenções, esquema de entidades, glossário, corpus anotado, pipeline de normalização e baseline.

## Estrutura

```
sprint1-pln/
├── sprint1_pln.ipynb           notebook executável (Colab T4)
├── corpus_enunciacoes.json     gerado pelo notebook depois da anotação
├── taxonomia_intencoes.json    intenções + mapeamento das 40 user stories
├── glossario_rodoviario.json   jargão, variantes, correções de ASR
├── DECISOES.md                 documento de decisões
├── USO_DE_IA.md                declaração do uso de IA
├── CHANGELOG.md
├── dados/
│   ├── esquema_entidades.json
│   ├── personas.csv              ← persona de cada áudio (da planilha de controle das gravações)
│   ├── schema_corpus.json      contrato de saída (gerado)
│   ├── transcricoes_brutas.csv       ← gerado pelo Whisper
│   ├── anotacao_a1.csv / anotacao_a2.csv   ← preenchidas pelos anotadores
│   ├── anotacao_final.csv            ← adjudicação das discordâncias
│   ├── transcricoes_oficiais.csv     ← transcrição feita ouvindo os áudios (referência do WER)
│   ├── transcricoes_brutas_large_v3.csv  ← Whisper large-v3 (revisão de acurácia)
│   ├── comparacao_wer_small_large.csv
│   └── baseline_small_vs_large.csv
├── src/                        código
└── tests/
```

## Como rodar

**Para reproduzir os resultados:** clone o repositório, instale o `requirements.txt` e execute o `sprint1_pln.ipynb` de dentro da pasta `sprint1-pln` (Jupyter), ou no Colab com a pasta no Drive em `MyDrive/challenge-motiva/sprint1-pln/`. As transcrições já estão em `dados/` (`dados/personas.csv`), então o notebook roda sem os áudios, que não vão para o repositório. Os passos abaixo descrevem o fluxo completo, desde a gravação.

1. Grave os áudios com o nome do id (`enu_0001.m4a` …) e coloque no Drive em `MyDrive/challenge-motiva/audios-sprint1/`.
2. Coloque esta pasta no Drive em `MyDrive/challenge-motiva/sprint1-pln/`.
3. Abra `sprint1_pln.ipynb` no Colab (ambiente com GPU T4) e execute tudo. A seção 3 transcreve, e a seção 4 cria as planilhas de anotação.
4. Cada anotador preenche a sua planilha **sem ver a outra**. Coluna `entidades`: `tipo=valor@trecho; ...` (ex.: `km=123.5@km 123.5; sentido=capital@sentido capital`).
5. Execute de novo: as seções 5 a 7 calculam o kappa, montam e validam o corpus e medem o baseline.
6. A seção 8 compara o Whisper small com o large-v3 (WER) e as regras v1 com as v2 (acurácia).

Testes: `python tests/test_normalizacao.py` e `python tests/test_corpus_kappa.py`.

## Status final (30/10/2026)

**Entregáveis:** taxonomia (40/40 user stories), esquema de entidades, glossário, corpus anotado (29 enunciações, kappa 0,717), pipeline de normalização e baseline de regras. Resultados, decisões e limitações no DECISOES.md.

**Revisão de acurácia (pedido do professor):** Whisper large-v3 (WER 35,0% → 27,5%) e regras v2 do baseline (v1 15/29 = 51,7%; v2 29/29 = 100,0%, número otimista). Detalhes no DECISOES.md, "Revisão de acurácia (30/10/2026)", e na seção 8 do notebook.

**Normalização numérica:** 14/16 = 87,5% → 16/16 = 100,0% (patamar ≥ 90%), com duas regras novas (ver DECISOES.md, "Revisão de acurácia").

**Pendências:** respostas do professor às perguntas em aberto do DECISOES.md; validação das regras v2 em gravações novas (Sprint 2).
