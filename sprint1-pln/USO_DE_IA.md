# Uso de IA nesta entrega

**Ferramenta:** Claude (Anthropic), modelo Claude Opus 5.5, via claude.ai, em 25/10/2026.

| Artefato | O que a IA fez | O que a aluna fez / precisa fazer |
|---|---|---|
| `taxonomia_intencoes.json` | Propôs as intenções, as fusões, as permissões e a criticidade a partir das 40 user stories. | Revisar e aprovar as fusões (DECISOES.md, D1). |
| `dados/esquema_entidades.json` | Propôs os formatos canônicos e as regras de normalização. | Revisar; decidir sobre `trecho` e `periodo`. |
| `glossario_rodoviario.json` | Rascunho inicial; as correções de ASR são hipóteses. | Completar com os erros reais observados nas transcrições do Whisper. |
| `roteiro/` | Escreveu as 60 frases. | Gravar os áudios. |
| `src/`, `tests/`, `sprint1_pln.ipynb` | Escreveu o código e os testes. | Executar no Colab e revisar. |
| Anotação do corpus | **Nenhuma participação.** A IA não anotou nem pré-anotou. | Anotação humana pelos dois anotadores. |
| `DECISOES.md` | Redigiu as justificativas. | Validar as decisões abertas (⚠️). |

A IA não gerou nenhum dado do corpus: os áudios, as transcrições (Whisper) e as anotações vêm da gravação e da anotação humanas.

## 27/10/2026
- A IA redigiu o fechamento das decisões no DECISOES.md conforme a decisão da aluna, gerou as planilhas de anotação em branco e o código de transcrição/WER. A transcrição oficial foi feita pela aluna ouvindo os áudios. A anotação é feita pela Pessoa 1 e pela Pessoa 2; a IA não anota nem pré-anota.

## Adjudicação (27/10/2026)
- O critério de adjudicação foi definido pela aluna (ficar com o rótulo mais próximo da transcrição oficial). A IA aplicou o critério às 7 discordâncias e redigiu os motivos; a escolha ficou sempre entre os rótulos dos dois anotadores humanos e foi registrada no DECISOES.md.
- A IA redigiu a seção "Resultados finais" do DECISOES.md a partir das saídas do notebook.

## Atualização (28 a 30/10/2026)

Ferramenta: assistente de IA Claude (Anthropic), no chat, sem acesso direto ao Drive. Todo código foi executado pela aluna no Colab, e os resultados conferidos por ela.

**Onde a IA foi usada nesta etapa:**
- Código das células auxiliares de: transcrição com o Whisper large-v3 e cálculo do WER contra a transcrição oficial; comparação do baseline com o Whisper small e o large-v3; organização da pasta de entrega.
- Regras v2 do baseline (`REGRAS_V2` em `src/baseline.py`), propostas pela IA a partir da análise dos erros da v1 no corpus, a pedido do professor para aumentar a acurácia. Por isso o DECISOES.md trata a acurácia da v2 como otimista.
- Duas regras novas de normalização numérica ("km de N" e horário com vírgula) e a atualização do trecho dessas duas entidades nas anotações convertidas, também a partir das falhas medidas.
- Redação dos textos que registram essas mudanças no DECISOES.md, no README.md e no CHANGELOG.md, revisados pela aluna.
- Experimento exploratório de classificação de intenção com um modelo de linguagem aberto (Qwen2.5-7B-Instruct) no Colab. Não faz parte da entrega, porque o enunciado da Sprint 1 não prevê modelo nesta etapa.

**O que não mudou e não foi feito pela IA nesta etapa:** os rótulos de intenção e entidades do corpus, a adjudicação e as decisões registradas no DECISOES.md. A troca do Whisper small pelo large-v3 foi sugestão do professor.
