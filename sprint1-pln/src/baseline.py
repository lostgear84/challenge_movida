"""Baseline obrigatório da Sprint 1.

Intenção: regras de palavras-chave (regex) com peso; vence a maior pontuação,
empate desfeito pela ordem de PRIORIDADE (mais específica primeiro).
Sem nenhuma regra disparada -> 'fora_de_escopo'.

Entidades: regex sobre o texto normalizado + busca das variantes do glossário.

As regras foram escritas a partir das user stories e do glossário, NÃO ajustadas
olhando o corpus anotado (para não inflar a acurácia). Ver DECISOES.md.
"""
import json
import re
from pathlib import Path

# (padrão, peso). O texto já chega normalizado (minúsculas, verbos no infinitivo).
REGRAS = {
    "confirmar": [(r"^(sim|confirmo|confirmar|positivo|correto|isso mesmo)\b", 3),
                  (r"^pode (registrar|enviar|encaminhar|mandar|seguir)\b", 3)],
    "negar_corrigir": [(r"^(não|negativo)\b", 3), (r"\b(errado|errada)\b", 1)],
    "cancelar": [(r"\b(cancelar|esquece|deixa para lá)\b", 3)],
    "registrar_direcionamento": [(r"\bdirecionamento\b", 4)],
    "validar_registro": [(r"\b(validar|aprovar)\b", 4)],
    "consultar_historico": [(r"\bhistórico\b", 4)],
    "consultar_procedimento": [(r"\b(procedimento|protocolo)\b", 3), (r"\bo que (eu )?faço\b", 2)],
    "registrar_dados_atendimento": [(r"\bpressão\b", 3), (r"\b(consciente|inconsciente|fratura|sangramento|corte no|lesão)\b", 2)],
    "gerar_resumo": [(r"\bgerar\b", 2), (r"\b(passagem de turno|síntese|relatório para)\b", 3),
                     (r"\bresumo do atendimento\b", 3)],
    "encerrar_atendimento": [(r"\b(encerrar|finalizar)\b", 3)],
    "consultar_pendencias": [(r"\b(incomplet\w*|pendente\w*|falta preencher|desvio\w*)\b", 3)],
    "consultar_indicadores": [(r"\b(tempo médio|comparar|desempenho|recorrent\w*|repetid\w*|volume)\b", 3)],
    "consultar_prioridades": [(r"\b(crític\w*|prioridade\w*|fora do prazo|atrasad\w*|há mais tempo)\b", 3)],
    "solicitar_apoio": [(r"\b(solicitar|preciso de|precisar de|apoio|reforço)\b", 2),
                        (r"\bmandar\b", 1)],
    "consultar_recursos": [(r"\b(acionad\w*|disponíve\w*|em uso)\b", 2),
                           (r"\b(onde est[áã]o?|quant[oa]s|quais|qual)\b.*\b(guinchos?|recursos?|viaturas?|ambulâncias?)\b", 2)],
    "consultar_dados_ocorrencia": [(r"\b(acesso|rota|risco\w*|como chego|interditad\w*)\b", 2),
                                   (r"\b(status|situação) da ocorrência\b", 3),
                                   (r"\bresumo da ocorrência\b", 3)],
    "consultar_panorama": [(r"\b(resumo|panorama)\b", 2), (r"\bcomo (tá|está) a operação\b", 3),
                           (r"\bquantas ocorrências\b", 2), (r"\bocorrências abertas\b", 2)],
    "relatar_condicoes": [(r"\binformar\b", 2),
                          (r"\b(neblina|chuva|pista molhada|vazando|carga|visibilidade|destruíd\w*)\b", 1)],
    "atualizar_status": [(r"\b(atualizar|mudar)\b.*\bstatus\b", 3),
                         (r"\b(cheguei|chegando|chegada|a caminho|saindo|missão recebida|em atendimento|iniciando|removid\w*|liberad\w*|marcar)\b", 2)],
    "registrar_ocorrencia": [(r"\b(registrar|abrir)\b.*\bocorrência\b", 3), (r"\b(registrar|abrir)\b", 1),
                             (r"\b(acidente|sinistro|batida|colisão|pane|animal na pista|veículo parado|carro parado)\b", 1)],
}
PRIORIDADE = list(REGRAS.keys())  # a ordem do dicionário é a prioridade de desempate


def classificar(texto):
    pontos = {}
    for intencao, regras in REGRAS.items():
        p = sum(peso for padrao, peso in regras if re.search(padrao, texto))
        if p:
            pontos[intencao] = p
    if not pontos:
        return "fora_de_escopo", {}
    melhor = max(pontos.values())
    empatadas = [i for i in PRIORIDADE if pontos.get(i) == melhor]
    return empatadas[0], pontos


class ExtratorEntidades:
    def __init__(self, caminho_glossario):
        g = json.loads(Path(caminho_glossario).read_text(encoding="utf-8"))
        self.variantes = []  # (tipo, canonico, variante) — variantes longas primeiro
        for t in g["termos"]:
            if t["tipo"] in ("tipo_ocorrencia", "recurso", "status", "condicao_observada"):
                for v in t["variantes"]:
                    self.variantes.append((t["tipo"], t["canonico"], v))
        self.variantes.sort(key=lambda x: -len(x[2]))

    def extrair(self, texto):
        ents, ocupado = [], []

        def livre(a, b):
            return all(b <= x or a >= y for x, y in ocupado)

        def add(tipo, valor, a, b):
            if livre(a, b):
                ents.append({"tipo": tipo, "valor": valor, "span": [a, b]})
                ocupado.append((a, b))

        for m in re.finditer(r"\bkm (\d+(?:\.\d+)?)\b", texto):
            add("km", float(m.group(1)), m.start(), m.end())
        for m in re.finditer(r"\b(?:sentido|pista) (capital|interior|litoral|norte|sul|leste|oeste|crescente|decrescente)\b", texto):
            add("sentido", m.group(1), m.start(), m.end())
        for m in re.finditer(r"\bfaixa (\d)\b", texto):
            add("faixa", f"faixa_{m.group(1)}", m.start(), m.end())
        for m in re.finditer(r"\bfaixa da (direita|esquerda)\b", texto):
            add("faixa", f"faixa_{m.group(1)}", m.start(), m.end())
        for m in re.finditer(r"\bacostamento\b", texto):
            add("faixa", "acostamento", m.start(), m.end())
        for m in re.finditer(r"\bocorrência (\d{2,})\b", texto):
            add("tag_ocorrencia", m.group(1), m.start(), m.end())
        for m in re.finditer(r"\b(\d{2}:\d{2})\b", texto):
            add("horario", m.group(1), m.start(), m.end())
        for tipo, canonico, v in self.variantes:
            for m in re.finditer(rf"\b{re.escape(v)}\b", texto):
                add(tipo, canonico, m.start(), m.end())
        return sorted(ents, key=lambda e: e["span"][0])


# ---------------------------------------------------------------- regras v2
# Versão 2 (30/10/2026), feita a pedido do professor para aumentar a acurácia.
# Diferente da v1, foi escrita DEPOIS da análise de erros do corpus anotado:
# cobre formas da fala real que a v1 não previa (1ª pessoa e particípios dos verbos,
# sinônimos de ocorrência, pedido de recurso, pergunta com período, relatório).
# Por isso a acurácia da v2 medida neste mesmo corpus é otimista (ver DECISOES.md).
# A v1 (REGRAS) continua igual e é a régua original da sprint.
REGRAS_V2 = {k: list(v) for k, v in REGRAS.items()}
REGRAS_V2["registrar_ocorrencia"] += [
    (r"\b(registro|registrei|registra|abro|abri)\b.*\bocorrência\b", 3),
    (r"\b(tombamento|tombad\w*|capotamento|capotad\w*|animal morto|atropelamento|incêndio|furad\w*|quebrad\w*)\b", 1),
    (r"\b(carro|veículo|caminhão|moto|ônibus)\b.*\bacostamento\b", 1),
]
REGRAS_V2["solicitar_apoio"] += [
    (r"\bprecis\w* d[eoa]s? (mais )?(um |uma )?(ambulância|guincho|helicóptero|equipe|viatura|apoio|reforço|resgate)\b", 3),
    (r"\bambulância\b", 1),
]
REGRAS_V2["encerrar_atendimento"] += [(r"\b(encerrad\w*|finalizad\w*)\b", 3)]
REGRAS_V2["consultar_recursos"] += [
    (r"\b(livres?|disponíve\w*)\b", 2),
    (r"\b(onde est[áã]o?|quant[oa]s|quais|qual)\b.*\bequipes?\b", 2),
]
REGRAS_V2["consultar_dados_ocorrencia"] += [(r"\bjá (resolveram|resolvid\w*|chegou|foi)\b", 3)]
REGRAS_V2["consultar_indicadores"] += [(r"\b(quant\w*|teve|tivemos)\b.*\b(semana|mês|meses|dias|período)\b", 3)]
REGRAS_V2["gerar_resumo"] += [(r"\brelatório\b", 3)]
REGRAS_V2["consultar_panorama"] += [(r"\bcomo\b.*\b(está|tá|anda)\b.*\boperação\b", 3)]


def classificar_v2(texto):
    """Mesmo critério de pontuação e desempate da v1, com as regras v2."""
    pontos = {}
    for intencao, regras in REGRAS_V2.items():
        p = sum(peso for padrao, peso in regras if re.search(padrao, texto))
        if p:
            pontos[intencao] = p
    if not pontos:
        return "fora_de_escopo", {}
    melhor = max(pontos.values())
    empatadas = [i for i in PRIORIDADE if pontos.get(i) == melhor]
    return empatadas[0], pontos
