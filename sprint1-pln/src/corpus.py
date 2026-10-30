"""Montagem do corpus_enunciacoes.json a partir das transcrições e das anotações.

Formato das planilhas de anotação (uma por anotador, preenchidas sem ver a outra):
  id, texto_normalizado, intencao, entidades
coluna 'entidades': itens separados por ';' no formato  tipo=valor@trecho
  ex.: km=123.5@km 123.5; sentido=capital@sentido capital
O 'trecho' é copiado do texto_normalizado; o código calcula o span sozinho.
"""
import csv
from collections import Counter
from pathlib import Path

from normalizacao import localizar_span

CAMPOS_ANOTACAO = ["id", "texto_normalizado", "intencao", "entidades"]


def ler_csv(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def gerar_planilhas_anotacao(transcricoes, pasta, anotadores=("a1", "a2")):
    """Cria uma planilha em branco por anotador. Não traz a intenção pretendida
    do roteiro, para não enviesar a anotação."""
    for a in anotadores:
        caminho = Path(pasta) / f"anotacao_{a}.csv"
        if caminho.exists():
            print(f"já existe, não sobrescrevi: {caminho}")
            continue
        with open(caminho, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CAMPOS_ANOTACAO)
            w.writeheader()
            for t in transcricoes:
                w.writerow({"id": t["id"], "texto_normalizado": t["texto_normalizado"],
                            "intencao": "", "entidades": ""})
        print(f"criada: {caminho}")


def _valor(tipo, v):
    v = v.strip()
    return float(v) if tipo == "km" else v


def parse_entidades(celula, texto):
    ents = []
    for item in filter(None, (x.strip() for x in (celula or "").split(";"))):
        tipo_valor, trecho = item.split("@", 1)
        tipo, valor = tipo_valor.split("=", 1)
        tipo = tipo.strip()
        ents.append({"tipo": tipo, "valor": _valor(tipo, valor),
                     "span": localizar_span(texto, trecho.strip())})
    return sorted(ents, key=lambda e: e["span"][0])


def concordancia_entidades(e1, e2):
    """F1 entre os conjuntos (tipo, valor) dos dois anotadores."""
    s1 = Counter((e["tipo"], e["valor"]) for e in e1)
    s2 = Counter((e["tipo"], e["valor"]) for e in e2)
    if not s1 and not s2:
        return 1.0
    comum = sum((s1 & s2).values())
    return 2 * comum / (sum(s1.values()) + sum(s2.values()))


def montar_corpus(transcricoes, personas, an1, an2, final, taxonomia, nomes=("a1", "a2")):
    """transcricoes: [{id, transcricao_bruta, texto_normalizado}]
    personas: {id: persona}
    an1, an2: anotações de cada anotador; final: anotação adjudicada (pode ser None).
    Sem 'final', só entram no corpus os itens em que os dois concordam na intenção."""
    tax = {i["nome"]: i for i in taxonomia["intencoes"]}
    a1 = {r["id"]: r for r in an1}
    a2 = {r["id"]: r for r in an2}
    fin = {r["id"]: r for r in (final or [])}
    corpus, pendentes = [], []
    for t in transcricoes:
        i = t["id"]
        if i not in a1 or i not in a2 or not a1[i]["intencao"] or not a2[i]["intencao"]:
            pendentes.append((i, "falta anotação"))
            continue
        concorda = a1[i]["intencao"].strip() == a2[i]["intencao"].strip()
        ref = fin.get(i) or (a1[i] if concorda else None)
        if ref is None:
            pendentes.append((i, "intenções diferentes: adjudicar em anotacao_final.csv"))
            continue
        intencao = ref["intencao"].strip()
        corpus.append({
            "id": i,
            "persona": personas[i],
            "transcricao_bruta": t["transcricao_bruta"],
            "texto_normalizado": t["texto_normalizado"],
            "intencao": intencao,
            "entidades": parse_entidades(ref["entidades"], t["texto_normalizado"]),
            "exige_confirmacao": tax[intencao]["exige_confirmacao"] if intencao in tax else False,
            "anotadores": list(nomes),
            "concordancia": 1.0 if concorda else 0.0,
        })
    return corpus, pendentes


def estatisticas(corpus):
    tokens = [r["texto_normalizado"].split() for r in corpus]
    vocab_bruto = Counter(w for r in corpus for w in r["transcricao_bruta"].lower().split())
    vocab = Counter(w for ts in tokens for w in ts)
    return {
        "n_enunciacoes": len(corpus),
        "vocabulario_bruto": len(vocab_bruto),
        "vocabulario_normalizado": len(vocab),
        "comprimento_medio_tokens": round(sum(map(len, tokens)) / max(len(tokens), 1), 2),
        "distribuicao_intencao": dict(Counter(r["intencao"] for r in corpus).most_common()),
        "distribuicao_persona": dict(Counter(r["persona"] for r in corpus).most_common()),
        "palavras_mais_frequentes": vocab.most_common(20),
    }
