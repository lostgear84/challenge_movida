# Changelog — sprint1-pln

## 2026-10-25 — versão 0.1 (rascunho)
Criado:
- `taxonomia_intencoes.json`: 21 intenções (17 de domínio + 4 transversais), 40/40 user stories mapeadas.
- `dados/esquema_entidades.json`: 9 tipos de entidade com formato canônico; `dados/schema_corpus.json` (contrato, gerado pelo código).
- `glossario_rodoviario.json`: termos, variantes, verbos de comando, correções de ASR (hipóteses), hesitações.
- `roteiro/roteiro_gravacao.csv` (com intenção) e `roteiro/frases_para_gravar.csv` (sem intenção): 60 frases.
- `src/normalizacao.py`, `baseline.py`, `kappa.py`, `validacao.py`, `corpus.py`, `metricas.py`, `transcricao.py`.
- `tests/`: 15 casos de normalização + kappa (conferido com o scikit-learn), corpus e validação.
- `sprint1_pln.ipynb`: pipeline de ponta a ponta. Executado localmente sem dados, e numa simulação com dados fictícios (descartados).
- `DECISOES.md`, `README.md`.

## 2026-10-25 — versão 0.1.1
- `src/transcricao.py`: passou a aceitar `.mp4` e `.aac` (formatos em que o WhatsApp exporta áudio). Antes, esses arquivos eram ignorados.
- `.gitignore`: bloqueia também `.mp4` e `.aac`.

## 2026-10-26 — versão 0.1.2
- Notebook (seção 4, planilhas de anotação): a persona de cada `enu_` passa a vir de `challenge-motiva/controle_gravacoes.xlsx`, e não mais do roteiro `frases_para_gravar.csv`. Motivo: o corpus é de falas livres, que não seguem as frases do roteiro. O notebook avisa quais ids ainda estão sem persona.
- Corpus: 14 áudios (`enu_0001` a `enu_0014`) em `audios-sprint1`; os arquivos originais do WhatsApp estão em `_arquivados`.
- Descartados: os 2 áudios de 25/10 (`WhatsApp Audio 2026-10-25 …`), apagados do Drive.
- Onde paramos: pasta organizada e código pronto para transcrever. Falta: persona do `enu_0001` ao `enu_0011` na planilha de controle; gravar os demais áudios até 60; rodar a transcrição.

## 2026-10-27 — versão 0.1.3 (corpus)
- Lote 2: 15 áudios gravados pela Sarah em 26/10, das 22:01 às 22:02 (`enu_0015` a `enu_0029`): supervisor (0015–0019), gerente (0020–0024) e APH (0025–0029). Linhas incluídas em `controle_gravacoes.xlsx`.
- A ordem dos áudios foi deduzida pela duração (as frases curtas caíram nos áudios curtos). Conferir na transcrição antes de anotar.
- Descartados: os 2 áudios das 22:04 de 26/10 (não entram no corpus).
- Decisão: o corpus fica com 29 enunciações, abaixo das 60 do enunciado. Registrar como limitação no `DECISOES.md`.
- Onde paramos: corpus fechado (29 áudios, 5 personas). Falta: rodar a transcrição e conferir a ordem do lote 2 e o par enu_0012/enu_0013; segundo anotador; fusões da taxonomia e entidades `trecho`/`periodo`; anotação, kappa e baseline.

## 2026-10-27 — versão 0.1.4
- `src/transcricao.py`: nova função `carregar_audio`, que lê o áudio direto do arquivo com o ffmpeg (mono, 16 kHz) e entrega o sinal pronto ao Whisper. Antes, o arquivo era passado ao ffmpeg por streaming, o que falhava com `.mp4` (o índice do mp4 fica no fim do arquivo) e gerava "Soundfile is either not in the correct format". A versão 0.1.1 tinha liberado a extensão `.mp4` sem corrigir a leitura.
- Onde paramos: transcrição dos 29 áudios. Falta: conferir as transcrições (ordem do lote 2 e par enu_0012/enu_0013), segundo anotador, decisões da taxonomia, anotação, kappa e baseline.

## 2026-10-27 — versão 0.1.5 (transcrição oficial)
- Novo `dados/transcricoes_oficiais.csv`: transcrição oficial dos 29 áudios, feita pela Sarah ouvindo cada um, ao lado da transcrição bruta do Whisper e do WER por frase. O `transcricoes_brutas.csv` não foi alterado.
- Decisão: na transcrição oficial, os números ficam escritos como foram falados (ex.: "cento e quarenta e três e meio"), para servir de teste ao normalizador de números.
- Confirmado: enu_0012 = inspetor (P1), enu_0013 = guincho 2, enu_0014 = resgate 07. A ordem do lote 2 (enu_0015 a enu_0029) bate com o roteiro.
- WER do Whisper small no corpus: 35.0%. Valor inflado: o Whisper escreve números em algarismos e a referência por extenso. Recalcular depois do normalizador.
- Onde paramos: transcrição oficial gravada. Falta: confirmar a forma falada nos enu_0012, enu_0013 e enu_0014 (coluna `conferir`); segundo anotador; decisões da taxonomia e entidades; anotação, kappa e baseline.

## 27/10/2026 — versão 0.1.6 (decisões fechadas e anotação)
- `taxonomia_intencoes.json` v0.2 (fusões aprovadas); `dados/esquema_entidades.json` v0.2 (entidades `trecho` e `periodo`); `glossario_rodoviario.json` (P1 = Persona 1).
- Novas `dados/anotacao_pessoa1.xlsx` e `dados/anotacao_pessoa2.xlsx`: texto do Whisper normalizado, lista de intenções e guia de anotação.
- DECISOES.md e README.md atualizados.
- Onde paramos: anotação. Falta: as duas pessoas anotarem; converter para CSV e executar o notebook; adjudicar; registrar os resultados.

## 27/10/2026 — versão 0.1.7
- `sprint1_pln.ipynb`: a célula de configuração passa a pôr a raiz do projeto no `sys.path`. No Colab a pasta de trabalho é `/content`, e a seção 2 não achava `tests/` (o notebook só tinha sido executado localmente, dentro da pasta do projeto).
- Onde paramos: anotações convertidas (`anotacao_a1.csv`, `anotacao_a2.csv`). Falta: executar o notebook; adjudicar as 7 discordâncias; registrar os resultados finais.

## 27/10/2026 — versão 0.1.8 (adjudicação)
- Novo `dados/anotacao_final.csv`: rótulo final das 7 frases em que os anotadores discordaram. Critério e motivos no DECISOES.md.
- Resultados antes da adjudicação (22 frases): kappa 0,717 (passa), F1 de entidades 0,784, baseline 8/22 = 36,4%, normalização numérica 10/12 = 83,3% (abaixo de 90%), aviso de governança na enu_0028 (APH encerrando atendimento).
- Onde paramos: adjudicação gravada. Falta: executar o sprint1_pln.ipynb de novo (corpus com 29 frases); levar as perguntas ao professor; registrar os números finais e as respostas no DECISOES.md.

## 27/10/2026 — versão 0.1.9 (resultados finais)
- Notebook executado com o corpus completo: 29 registros, 0 pendentes, 0 erros de schema; kappa 0,717; F1 de entidades 0,784; baseline 12/29 = 41,4%; normalização 14/16 = 87,5% (abaixo de 90%); avisos de governança na enu_0016 e na enu_0028.
- DECISOES.md (resultados finais, limitações, perguntas ao professor) e README.md atualizados.
- Onde paramos: sprint fechada do lado técnico. Falta: respostas do professor e os ajustes que dependerem delas.

## 27/10/2026 — versão 0.1.10 (governança)
- `taxonomia_intencoes.json` v0.2.1: campo `politica_fora_de_permissao` (pedido fora da permissão é recusado e redirecionado). As permissões não mudaram.
- DECISOES.md: D11, com os casos enu_0016 e enu_0028 como testes de recusa. Rótulos do corpus inalterados.
- Onde paramos: Sprint 1 fechada do lado técnico. Falta: respostas do professor; implementar a recusa no agente (Sprint 2).

## 27/10/2026 — versão 0.1.11 (documentação)
- Revisão de texto do DECISOES.md, README.md e CHANGELOG.md.
- `sprint1_pln.ipynb`: removidas células auxiliares que tinham sido coladas depois do resumo das métricas.

## 29/10/2026 — Whisper large-v3 (comparação com o small)
- Sugestão do professor: trocar o Whisper small pelo large-v3 para melhorar a acurácia do baseline e o F1 de entidades.
- Novos `dados/transcricoes_brutas_large_v3.csv` e `dados/comparacao_wer_small_large.csv` (WER por frase, mesma regra para os dois modelos).
- WER: small 35.0% | large-v3 27.5% (referência: coluna `transcricao_oficial` da transcrição oficial).
- Baseline (mesmos rótulos de intenção): small 12/29 = 41.4% | large-v3 15/29 = 51.7%. Detalhe em `dados/baseline_small_vs_large.csv`.
- Onde paramos: transcrição e WER do large-v3 prontos; corpus ainda sobre o small. Falta: conferir o formato das entidades, passar o corpus para o large-v3, rodar o sprint1_pln.ipynb e registrar o antes/depois no DECISOES.md.

## 30/10/2026 — versão 0.2.0 (revisão de acurácia e fechamento)
- `src/baseline.py`: regras v2 (`REGRAS_V2`, `classificar_v2`), escritas depois da análise de erros do corpus; a v1 não mudou. Acurácia v2: small 26/29 = 89,7% | large-v3 29/29 = 100,0% (otimista: medida no corpus usado para ajustar).
- Decisão: o corpus continua sobre o texto do Whisper small, porque os trechos das entidades foram marcados nesse texto. O large-v3 entra como comparação.
- `sprint1_pln.ipynb`: nova seção 8 (WER small × large-v3; regras v1 × v2), resumo das métricas com os números novos, retirado o pré-teste no texto do roteiro (o roteiro serviu só para gravar e não faz parte da entrega).
- `DECISOES.md`: seção "Revisão de acurácia (30/10/2026)", com o método da anotação (ouvindo os áudios); D4, D9, D10 e "Resultados finais" atualizados.
- `README.md`: estrutura sem a pasta `roteiro/`, com os arquivos novos, e status final.
- Onde paramos: Sprint 1 fechada. Falta: respostas do professor; validar as regras v2 em gravações novas (Sprint 2).

## 30/10/2026 — versão 0.2.1 (normalização numérica)
- `src/normalizacao.py` (`regras_dominio`): "km de N" vira "km N"; horário com vírgula ("14,32") vira "14:32". Regras tiradas das duas falhas da medição anterior.
- Normalização numérica: 14/16 = 87,5% → 16/16 = 100,0% (patamar ≥ 90%). Número otimista, pelo mesmo motivo da v2.
- `dados/anotacao_a1.csv` e `anotacao_a2.csv`: o trecho das entidades km da enu_0001 e horário da enu_0013 passou para a forma do texto novo. Tipo e valor não mudaram; kappa (0,717) e F1 (0,784) conferidos, iguais. As planilhas `.xlsx` não mudaram.
- `tests/test_normalizacao.py`: dois casos novos.
- Onde paramos: Sprint 1 fechada. Falta: respostas do professor; validar as regras novas em gravações novas (Sprint 2).

## 30/10/2026 — versão 0.2.2 (formato de entrega)
- `USO_DE_IA.md` de volta ao projeto (exigido no formato de entrega), com a atualização de 28 a 30/10/2026.

## 30/10/2026 — versão 0.2.3 (reprodutibilidade)
- `sprint1_pln.ipynb`: a configuração acha a pasta do projeto sozinha (pasta atual, para quem clona o repositório, ou o Drive no Colab), em vez de um caminho fixo do Drive.
- Novo `dados/personas.csv` (id e persona de cada áudio, extraído da planilha de controle das gravações). A seção 4 passa a ler dele, e o notebook não depende mais de arquivos fora da pasta do projeto. Conferido: as personas são as mesmas do corpus.
- README: como reproduzir os resultados.
