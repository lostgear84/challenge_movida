# Documento de decisões — Sprint 1 (PLN)

Status: as decisões marcadas com ⚠️ foram fechadas (ver as seções de 27/10/2026 no fim do documento).

## D1. Taxonomia: 17 intenções de domínio \+ 4 transversais

As 40 user stories viraram 17 intenções de domínio. A regra usada foi: **mesma ação \= mesma intenção, mesmo que mude a persona**. O que muda entre personas é a permissão, que fica em `personas_autorizadas`.

Fusões feitas (todas documentadas em `mapeamento_user_stories` na taxonomia):

| Intenção | Stories fundidas | Por quê |
| :---- | :---- | :---- |
| `solicitar_apoio` | P1-US6, P2-US6, P3-US5 | Exemplo dado pelo próprio enunciado: a mesma ação em três personas. |
| `atualizar_status` | P1-US5, P2-US2, P2-US4, P2-US7, P3-US3, P3-US6 | "Confirmar recebimento", "registrar chegada" e "marcar horários" são mudanças de etapa. O horário é marcado automaticamente em cada atualização, e a etapa vira a entidade `status`. Separar em seis intenções geraria discordância alta entre anotadores. |
| `relatar_condicoes` | P1-US3, P2-US5 | As duas descrevem local/via/veículo para complementar uma ocorrência. |
| `consultar_procedimento` | P1-US2, P3-US1 | Procedimento e protocolo são consultas à mesma base aprovada. |
| `consultar_dados_ocorrencia` | P2-US1, P2-US3, P3-US4 | Resumo da missão, rota/acesso e dados da ocorrência são perguntas sobre a ocorrência. |
| `consultar_recursos` | P1-US4, P4-US3, P5-US6 | O foco da pergunta é o recurso. |
| `encerrar_atendimento` | P1-US8, P2-US8 | Encerrar e finalizar missão são o mesmo ato. |
| `gerar_resumo` | P3-US8, P4-US8, P5-US7 | Pedem um documento editável para revisar e enviar (critério transversal 8). O tipo de resumo pode virar entidade depois. |
| `consultar_panorama` | P1-US7, P4-US1, P5-US1 | Visão geral do momento. |
| `consultar_prioridades` | P4-US2, P4-US5, P5-US2 | Filtro de urgência. |
| `consultar_indicadores` | P4-US4, P5-US3, P5-US4 | Perguntas analíticas. |
| `consultar_pendencias` | P3-US7, P5-US5 | O que está faltando ou fora do padrão. |

Ficaram sozinhas: `registrar_ocorrencia`, `registrar_dados_atendimento` (separada por ter dado de saúde, protegido pela LGPD), `consultar_historico`, `validar_registro` e `registrar_direcionamento`.

As intenções transversais (`confirmar`, `negar_corrigir`, `cancelar`, `fora_de_escopo`) não vêm de user story. Elas existem para cumprir os critérios transversais 1 (pedir esclarecimento) e 2 (confirmar antes de agir).

## D2. Alerta de exceção (P4-US5) fora da camada de NLU

O alerta é disparado pelo sistema, não pela fala do usuário. A parte falada (perguntar se há algo fora do prazo) foi mapeada para `consultar_prioridades`. O alerta automático entra na Sprint 3 (agente proativo).

## D3. Criticidade e confirmação

- **Alta** (cria, aciona, encerra ou valida; ou envolve dado sensível) → exige confirmação.  
- **Média** (altera registro ou gera documento para envio) → exige confirmação.  
- **Baixa** (só consulta) → não exige confirmação.

A regra segue a premissa da Motiva: "confirmação explícita antes de ações críticas, envios ou encerramentos".

## D4. Entidades

São os 9 tipos do enunciado, cada um com valor canônico (ver `dados/esquema_entidades.json`). Duas escolhas:

- "Óleo na pista" é `tipo_ocorrencia`, não `condicao_observada`, para que o mesmo trecho não receba dois rótulos.  
- `trecho` ("trecho sul") e `periodo` ("deste mês") aparecem nas falas de supervisor e gerente, mas não estão na lista do enunciado. Entraram como extensão (decisão de 27/10/2026).  

## D5. Spans

O exemplo do enunciado (`span: [21, 42]`) não bate com nenhum dos dois textos do próprio exemplo. Adotamos: **posições \[início, fim) sobre o `texto_normalizado`**, fim exclusivo como em Python. O código calcula o span sozinho a partir do trecho copiado pelo anotador, o que evita erro de contagem manual.

## D6. Normalização

- Números por extenso viram dígitos, respeitando a composição do português: "cento e vinte e três" vira 123, mas "quinze e quarenta" não vira 55 (permanece "15 e 40", que depois vira 15:40 depois de "às").  
- Dígitos falados um a um são concatenados: "três quatro sete" vira 347, e "meia" vale 6 dentro dessa sequência.  
- "um/uma" só vira 1 depois de km, faixa, às ou ocorrência. Assim "uma ocorrência" continua artigo.  
- km: "e meio" soma 0.5, "mais 300" soma 300 m (51.3), e "123,5" e "51+300" do próprio Whisper também são tratados.  
- Hesitações e os marcadores "aí", "ó" e "né" são removidos, e os verbos de comando vão para o infinitivo (registra → registrar).  
- "pra/pro" viram "para/para o".  
- ⚠️ "às duas horas" vira 02:00 (sem AM/PM). Dá para inferir pelo contexto depois.  
- O exemplo do enunciado também remove o artigo ("registrar ocorrência"). Não removemos artigos de forma geral, porque isso apagaria informação ("uma viatura").

## D7. Concordância

- **Kappa:** calculado sobre a intenção (geral) e por intenção, comparando aquela intenção com todas as outras (binário). O gate pega as intenções com kappa \< 0,70.  
- **Campo `concordancia` de cada registro:** 1.0 se os dois anotadores deram a mesma intenção, 0.0 se não.  
- **Entidades:** concordância medida à parte, pelo F1 entre os conjuntos (tipo, valor).  
- Discordâncias são resolvidas em `dados/anotacao_final.csv` (adjudicação), e o registro guarda concordancia \= 0.0.  
- **Achado da simulação:** com 1 a 4 exemplos por intenção, uma única discordância já derruba o kappa daquela intenção abaixo de 0,70. O kappa por intenção é instável com um corpus deste tamanho. Isso deve ser reportado como limitação, e as intenções com 1 exemplo são candidatas a fusão no gate.

## D8. Dados e privacidade

- Os áudios ficam no Drive e nunca no repositório (`.gitignore`), porque voz é dado pessoal. Só o texto transcrito é versionado.  
- As frases de APH usam dados clínicos **fictícios**.

## D9. Gravação

- As gravações foram orientadas por um roteiro de apoio de 60 frases, cobrindo as 21 intenções. O roteiro serviu só para gravar e não faz parte da entrega; o corpus final tem 29 enunciações (ver 27/10/2026).  
- Na anotação, cada anotador rotula o que foi dito no áudio, e não o roteiro.

## D10. Baseline

As palavras-chave da versão 1 (v1) foram escritas a partir das user stories e do glossário, sem olhar o corpus anotado. A acurácia oficial é medida no corpus anotado, com as transcrições reais do Whisper. A versão 2 (v2), escrita depois da análise de erros, está em "Revisão de acurácia (30/10/2026)".

- **D1 (taxonomia):** fusões aprovadas como propostas. `taxonomia_intencoes.json` passa para a versão 0.2.  
- **D4 (entidades):** `trecho` e `periodo` entram como entidades (extensão do enunciado, justificada pelas falas de supervisor e gerente: "trecho norte", "nos últimos trinta dias"). `esquema_entidades.json` passa para a versão 0.2.  
- **Segundo anotador:** Pessoa 2, integrante humano. Cada pessoa anota a sua planilha (`dados/anotacao_pessoa1.xlsx` e `dados/anotacao_pessoa2.xlsx`) sem ver a outra.  
- **P1:** interpretado como Persona 1 (Agente de Inspeção de Tráfego), mesma numeração das user stories. O áudio enu\_0012 ("aqui é o inspetor P1") é coerente com isso.  
- **D9 (corpus):** 29 enunciações das 5 personas, abaixo das 60 do enunciado (limitação). As gravações têm mais de uma voz (ver `controle_gravacoes.xlsx`), o que reduz a limitação de voz única.  
- **Transcrição oficial:** `dados/transcricoes_oficiais.csv`, feita ouvindo os áudios, com os números escritos como foram falados. Serve de referência para o WER do Whisper. O corpus anotado continua usando a transcrição do Whisper normalizada (D9), porque é o que o sistema recebe em produção.  
- **Glossário e erros reais do ASR:** os erros observados ("guicho"/"guinche" → guincho, "cincha/sinche/cinchido do" → sentido, "acustamento" → acostamento, "D.A.P."/"ap") ficam registrados como achado, mas **não** entram nas `correcoes_asr` nesta sprint. Ajustar o glossário com o próprio corpus de avaliação inflaria a acurácia do baseline (D10). Entram na Sprint 2, avaliados em dados novos.

## Adjudicação (27/10/2026)

Critério definido pela aluna: em cada discordância, fica a intenção mais próxima do que foi realmente dito (transcrição oficial, `dados/transcricoes_oficiais.csv`), aplicando a regra de desempate da taxonomia. A escolha é sempre entre os rótulos dos dois anotadores. As entidades seguem o mesmo critério: ficam as que correspondem ao que foi dito, de qualquer um dos dois. O kappa (0,717) foi calculado antes da adjudicação, e essas frases ficam no corpus com `concordancia = 0.0`.

| id | Pessoa 1 | Pessoa 2 | Final | Motivo (transcrição oficial) |
| :---- | :---- | :---- | :---- | :---- |
| enu\_0005 | registrar\_ocorrencia | relatar\_condicoes | registrar\_ocorrencia | Relata um acidente novo. Entidades da Pessoa 2: "km 15 23" não corresponde ao km falado (153). |
| enu\_0008 | registrar\_ocorrencia | solicitar\_apoio | registrar\_ocorrencia | Relata um veículo com pneu furado; não pede recurso específico. |
| enu\_0011 | atualizar\_status | solicitar\_apoio | solicitar\_apoio | "Precisa de ambulância" é o pedido que gera ação. Frase com mais de uma intenção (chegada \+ pedido): limitação. Entidades das duas anotações. |
| enu\_0014 | solicitar\_apoio | relatar\_condicoes | solicitar\_apoio | "Preciso de mais uma ambulância no local com urgência." |
| enu\_0015 | consultar\_dados\_ocorrencia | consultar\_recursos | consultar\_dados\_ocorrencia | A pergunta principal é "qual o status da ocorrência". |
| enu\_0016 | registrar\_direcionamento | solicitar\_apoio | solicitar\_apoio | "Manda a viatura de sinalização dois pro km 210" é pedido de recurso. A taxonomia não dá essa intenção ao supervisor: lacuna de permissão (pergunta ao professor). |
| enu\_0018 | consultar\_panorama | gerar\_resumo | consultar\_panorama | "Me passa um resumo" é pedido falado; quase igual ao exemplo da própria intenção. |

## Resultados finais (27/10/2026)

Corpus: 29 enunciações (5 personas), 0 pendentes, 0 erros de schema. Transcrição: Whisper small (`openai/whisper-small`, Hugging Face Transformers), português fixo, CPU no Colab.

| Métrica | Resultado | Patamar | Situação |
| :---- | :---- | :---- | :---- |
| Cobertura da taxonomia | 40/40 \= 100% | 100% | atingido |
| Kappa das intenções (antes da adjudicação) | 0,717 | ≥ 0,70 | atingido |
| Concordância de entidades (F1 médio) | 0,784 | extra | — |
| Acurácia do baseline (29 frases) | 12/29 \= 41,4% | reportada | — |
| Normalização numérica | 14/16 \= 87,5% → 16/16 \= 100,0% (revisão de 30/10/2026) | ≥ 90% | atingido na revisão |

**Gate por intenção:** 7 intenções ficaram com kappa \< 0,70 (solicitar\_apoio 0,583; consultar\_dados\_ocorrencia, consultar\_panorama, consultar\_recursos e gerar\_resumo 0,651; relatar\_condicoes e registrar\_direcionamento 0). Com 1 a 7 exemplos por intenção, uma discordância derruba o valor (achado previsto em D7). Reportado como limitação; fusões dependem da orientação do professor.

**Baseline (regras v1):** 12/29 nas transcrições reais. A maioria dos erros cai em `fora_de_escopo` (nenhuma regra dispara). Causa principal: a fala real usa formas que as regras não cobrem ("registro uma ocorrência", 1ª pessoa) e o ASR corrompe palavras-chave. É a principal justificativa para a abordagem com LLM na Sprint 2\.

**Normalização:** as 2 falhas têm causa conhecida: "km de 143 e meio" (o "de" quebra a regra do km) e o horário "14,32" escrito com vírgula pelo Whisper. Não foram corrigidas, para não ajustar as regras no próprio corpus de avaliação (D10). Na revisão de 30/10/2026 foram corrigidas (ver "Revisão de acurácia").

**Governança:** enu\_0016 (supervisor pedindo recurso) e enu\_0028 (APH encerrando atendimento) usam intenções que a taxonomia não autoriza para essas personas. A fala real mostrou lacunas de permissão nas user stories.

**Limitações:** corpus com 29 enunciações (o enunciado pede 60); distribuição desigual (12 frases de inspeção e 1 de guincho); frases com mais de uma intenção (enu\_0011); kappa por intenção instável com poucos exemplos.

**Perguntas em aberto para o professor:** (1) corpus de 29; (2) fundir ou só reportar as intenções abaixo de 0,70; (3) corrigir agora a normalização e o baseline, com número otimista, ou na Sprint 2, com dados novos (respondida em 30/10/2026: ver "Revisão de acurácia"); (4) confirmar a D11 (pedido fora da permissão é recusado e redirecionado); (5) P1 \= Persona 1; (6) entidades `trecho` e `periodo`; (7) corpus sobre a transcrição do Whisper; (8) códigos de ocorrência do KCOR (glossário, a\_confirmar).

## D11. Pedidos fora da permissão (27/10/2026)

Quando uma persona pede algo que não está autorizado para ela, o agente reconhece a intenção, **não executa**, explica que aquela função não pode fazer o pedido e oferece a alternativa permitida.

- **enu\_0016** (supervisor: "manda a viatura de sinalização dois pro km 210") → `solicitar_apoio` não é do supervisor. O agente não aciona e orienta que o pedido seja feito pela equipe de campo.  
- **enu\_0028** (APH: "atendimento encerrado no km 125") → `encerrar_atendimento` não é do APH. O agente não encerra a ocorrência e oferece marcar a etapa do APH como concluída (`atualizar_status`).

Os rótulos do corpus **não mudam**: os dois anotadores concordaram que é isso que a pessoa pediu, e a regra de governança age depois da classificação. Por isso o notebook continua apontando esses dois casos no aviso de governança: eles passam a ser **casos de teste** do comportamento de recusa, implementado na Sprint 2\.

## Revisão de acurácia (30/10/2026)

Resposta à pergunta (3): o professor pediu para aumentar a acurácia agora e sugeriu trocar o Whisper small pelo large-v3. Foram feitas duas mudanças, medidas contra os **mesmos rótulos de intenção** do corpus. A anotação e a adjudicação não mudaram.

**Método da anotação:** os dois anotadores rotularam cada frase ouvindo o áudio. A planilha trazia o texto normalizado do Whisper small, de onde os trechos das entidades foram copiados. Por isso os rótulos de intenção valem para qualquer transcrição do mesmo áudio.

1. **Transcrição com Whisper large-v3** (`openai/whisper-large-v3`, GPU T4 no Colab; `dados/transcricoes_brutas_large_v3.csv`). WER contra a transcrição oficial: small 35,0% → large-v3 27,5% (`dados/comparacao_wer_small_large.csv`). Parte do erro restante vem dos números, que a referência escreve por extenso e o Whisper em algarismos; isso pesa igual nos dois modelos.
2. **Regras v2 do baseline** (`classificar_v2` em `src/baseline.py`). A v1 não mudou.

| Classificador | Whisper small | Whisper large-v3 |
| :---- | :---- | :---- |
| Regras v1 (originais) | 12/29 = 41,4% | 15/29 = 51,7% |
| Regras v2 (revisão) | 26/29 = 89,7% | 29/29 = 100,0% |

**Meta pedida pelo professor (acurácia ≥ 80%):** atingida pelas regras v2 nas duas transcrições (26/29 = 89,7% com o Whisper small e 29/29 = 100,0% com o large-v3). As regras v1 ficam abaixo da meta e continuam registradas como a régua original. Leia a ressalva sobre a v2 no parágrafo seguinte.

**Leitura correta da v2:** as regras v2 foram escritas depois da análise dos erros da v1 neste mesmo corpus. Elas cobrem formas da fala real que a v1 não previa: verbos na 1ª pessoa e no particípio ("registro uma ocorrência", "atendimento encerrado"), sinônimos de ocorrência ("tombamento", "animal morto"), pedido de recurso ("precisa de ambulância"), perguntas com período ("essa semana", "últimos 30 dias") e "relatório". Por isso a acurácia da v2 medida aqui é **otimista** e não estima o desempenho em falas novas. A v1, escrita sem olhar o corpus, continua sendo a medida sem viés. A v2 será validada na Sprint 2, em gravações novas.

**Erros restantes da v2:** com o texto do large-v3, a v2 acerta 29 de 29 frases. Com o texto do small, erra enu_0006 ("carro do acustamento km 227 cinchido capital…"); enu_0008 ("tem um carro burado pneu aqui precisando de a…"); enu_0014 ("central desgato 07 aqui diamos o acidente sin…"). Nesses casos, o Whisper small corrompeu as palavras que as regras procuram.

**3. Normalização numérica (revisão):** duas regras novas em `regras_dominio` (`src/normalizacao.py`): "km de N" passa a ser lido como "km N" ("km de 143 e meio" → "km 143.5"), e um horário escrito com vírgula pelo Whisper ("14,32") passa a "14:32". As duas falhas da medição anterior eram exatamente esses casos (enu_0001 e enu_0013), e a taxa foi de 14/16 = 87,5% para 16/16 = 100,0%, acima do patamar de 90%. Como as regras saíram da análise das falhas deste corpus, esse número também é otimista, como o da v2. Nas duas frases o texto normalizado mudou, e o trecho dessas duas entidades foi atualizado para a forma nova nas anotações convertidas (`anotacao_a1.csv` e `anotacao_a2.csv`). O tipo e o valor anotados não mudaram, então o kappa e o F1 de entidades continuam iguais. As planilhas originais (`.xlsx`) não foram alteradas. `tests/test_normalizacao.py` ganhou um caso de teste para cada regra.

**O que não muda:** o kappa (0,717) e o F1 de entidades (0,784) medem a concordância entre os anotadores e não dependem da transcrição. O corpus (`corpus_enunciacoes.json`) continua sobre o texto do Whisper small, porque os trechos das entidades foram marcados nesse texto; trocar a transcrição exigiria remarcar os trechos sem os anotadores.

**Pré-teste do roteiro:** retirado do notebook. O roteiro serviu só para gravar e não faz parte da entrega.
