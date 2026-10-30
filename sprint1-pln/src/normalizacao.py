"""Pipeline de pré-processamento das transcrições do Whisper.

Etapas (na ordem):
 1. minúsculas + Unicode NFC
 2. hesitações escritas com reticências ("é...") e pontuação ausente/sobrando
 3. correções de erros recorrentes do ASR (glossário)
 4. remoção de hesitações e marcadores de discurso
 5. unidades (quilômetro -> km) e verbos de comando no infinitivo
 6. números por extenso -> dígitos (com regras de composição do português)
 7. regras do domínio: km com "e meio" / "mais N metros", horários HH:MM
"""
import json
import re
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------- números
UNIDADES = {"zero": 0, "um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "tres": 3,
            "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9}
DEZ_A_DEZENOVE = {"dez": 10, "onze": 11, "doze": 12, "treze": 13, "quatorze": 14,
                  "catorze": 14, "quinze": 15, "dezesseis": 16, "dezessete": 17,
                  "dezoito": 18, "dezenove": 19}
DEZENAS = {"vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50, "cinqüenta": 50,
           "sessenta": 60, "setenta": 70, "oitenta": 80, "noventa": 90}
CENTENAS = {"cem": 100, "cento": 100, "duzentos": 200, "duzentas": 200, "trezentos": 300,
            "trezentas": 300, "quatrocentos": 400, "quatrocentas": 400, "quinhentos": 500,
            "quinhentas": 500, "seiscentos": 600, "seiscentas": 600, "setecentos": 700,
            "setecentas": 700, "oitocentos": 800, "oitocentas": 800, "novecentos": 900,
            "novecentas": 900}
NUMEROS = {**UNIDADES, **DEZ_A_DEZENOVE, **DEZENAS, **CENTENAS}

# "um/uma" sozinhos são artigo ("uma ocorrência"); só viram 1 depois destes gatilhos
GATILHOS_UM = {"km", "faixa", "às", "ocorrência", "número"}


def _classe(v):
    if v < 10:
        return "unidade"
    if v < 20:
        return "dez_a_dezenove"
    if v < 100:
        return "dezena"
    return "centena"


def _permite(ultima, nova):
    """Composição válida em português: cento e vinte e três sim; quinze e quarenta não."""
    if ultima == "centena":
        return nova in ("dezena", "dez_a_dezenove", "unidade")
    if ultima == "dezena":
        return nova == "unidade"
    if ultima == "mil":
        return nova in ("centena", "dezena", "dez_a_dezenove", "unidade")
    return False


def _valor(tokens, i):
    """Valor numérico do token i, ou None. 'meia' só vale 6 numa sequência de dígitos."""
    w = tokens[i]
    if w in NUMEROS:
        return NUMEROS[w]
    if w == "mil":
        return 1000
    if w == "meia":
        ant = tokens[i - 1] if i > 0 else ""
        prox = tokens[i + 1] if i + 1 < len(tokens) else ""
        if ant != "e" and (ant in UNIDADES or prox in UNIDADES):
            return 6
    return None


def converter_numeros(tokens):
    """Converte números por extenso em dígitos. Dígitos falados um a um
    ("três quatro sete") são concatenados ("347")."""
    saida = []  # (texto, eh_digito_unico, palavra_original)
    i, n = 0, len(tokens)
    while i < n:
        v = _valor(tokens, i)
        if v is None:
            saida.append((tokens[i], False, tokens[i]))
            i += 1
            continue
        inicio = i
        if v == 1000:
            total, atual, ultima = 1000, 0, "mil"
        else:
            total, atual, ultima = 0, v, _classe(v)
        j = i + 1
        while j < n:
            k = j
            if tokens[k] == "e" and k + 1 < n and _valor(tokens, k + 1) is not None:
                k += 1
            v2 = _valor(tokens, k)
            if v2 is None:
                break
            if v2 == 1000 and ultima != "mil" and k == j:  # "dois mil"
                total += (atual or 1) * 1000
                atual, ultima = 0, "mil"
                j = k + 1
                continue
            c2 = _classe(v2) if v2 != 1000 else "mil"
            if _permite(ultima, c2):
                atual += v2
                ultima = c2
                j = k + 1
            else:
                break
        valor = total + atual
        unico = (j - inicio == 1) and valor < 10
        saida.append((str(valor), unico, tokens[inicio]))
        i = j

    # junta dígitos falados um a um e decide o "um/uma" isolado
    final, i = [], 0
    while i < len(saida):
        txt, unico, orig = saida[i]
        if unico:
            j = i
            while j + 1 < len(saida) and saida[j + 1][1]:
                j += 1
            if j > i:  # sequência de dígitos
                final.append("".join(s[0] for s in saida[i:j + 1]))
                i = j + 1
                continue
            if orig in ("um", "uma"):
                anterior = final[-1] if final else ""
                final.append(txt if anterior in GATILHOS_UM else orig)
                i += 1
                continue
        final.append(txt)
        i += 1
    return final


def _fmt(x):
    return ("%.3f" % x).rstrip("0").rstrip(".")


def regras_dominio(texto):
    # km: vírgula decimal e notação 51+300 do próprio ASR
    texto = re.sub(r"\bkm de (\d)", r"km \1", texto)          # "km de 143 e meio" -> "km 143 e meio" (v0.2.1)
    texto = re.sub(r"\bkm (\d+),(\d+)\b", r"km \1.\2", texto)
    texto = re.sub(r"\bkm (\d+)\s*\+\s*(\d{1,3})\b",
                   lambda m: "km " + _fmt(int(m.group(1)) + int(m.group(2)) / 1000), texto)
    texto = re.sub(r"\bkm (\d+) mais (\d{1,3})\b",
                   lambda m: "km " + _fmt(int(m.group(1)) + int(m.group(2)) / 1000), texto)
    texto = re.sub(r"\bkm (\d+) e meio\b", lambda m: "km " + _fmt(int(m.group(1)) + 0.5), texto)
    # horários
    def hora(h, m="0"):
        h, m = int(h), int(m)
        return f"{h:02d}:{m:02d}" if h < 24 and m < 60 else None
    texto = re.sub(r"(?<![\d.,])(\d{1,2}),(\d{2})(?![\d,])",  # horário com vírgula: "14,32" -> "14:32" (v0.2.1)
                   lambda m: hora(m.group(1), m.group(2)) or m.group(0), texto)
    texto = re.sub(r"\b(\d{1,2})h(\d{2})\b", lambda m: hora(m.group(1), m.group(2)) or m.group(0), texto)
    texto = re.sub(r"\bàs (\d{1,2}) e (\d{1,2})( minutos)?\b",
                   lambda m: ("às " + hora(m.group(1), m.group(2))) if hora(m.group(1), m.group(2)) else m.group(0), texto)
    texto = re.sub(r"\bàs (\d{1,2}) horas?\b",
                   lambda m: ("às " + hora(m.group(1))) if hora(m.group(1)) else m.group(0), texto)
    return texto


class Normalizador:
    def __init__(self, caminho_glossario):
        g = json.loads(Path(caminho_glossario).read_text(encoding="utf-8"))
        self.verbos = g["verbos_comando"]
        self.hesitacoes = set(g["hesitacoes"])
        self.marcadores = set(g["marcadores_discurso_removidos"])
        # correções de várias palavras primeiro
        self.correcoes = sorted(g["correcoes_asr"], key=lambda c: -len(c["errado"]))
        unidades = [t for t in g["termos"] if t["canonico"] == "km"][0]["variantes"]
        self.km_variantes = sorted(unidades, key=len, reverse=True)

    def normalizar(self, texto):
        t = unicodedata.normalize("NFC", texto).lower()
        t = re.sub(r"\bé\s*(\.\.\.|…)", " ", t)              # "é..." = hesitação
        t = re.sub(r"(\.\.\.|…)", " ", t)
        t = re.sub(r"(?<!\d)[.,]|[.,](?!\d)", " ", t)         # pontuação fora de números
        t = re.sub(r"[!?;:\"“”()\[\]]", " ", t)
        t = re.sub(r"\s+", " ", t).strip()
        for c in self.correcoes:
            t = re.sub(rf"\b{re.escape(c['errado'])}\b", c["certo"], t)
        for v in self.km_variantes:
            t = re.sub(rf"\b{re.escape(v)}\b", "km", t)
        tokens = [w for w in t.split() if w not in self.hesitacoes and w not in self.marcadores]
        tokens = [self.verbos.get(w, w) for w in tokens]
        tokens = converter_numeros(tokens)
        return regras_dominio(" ".join(tokens))


def localizar_span(texto, trecho):
    """[início, fim) da primeira ocorrência do trecho no texto (fim exclusivo)."""
    i = texto.find(trecho)
    if i < 0:
        raise ValueError(f"trecho '{trecho}' não encontrado em '{texto}'")
    return [i, i + len(trecho)]
