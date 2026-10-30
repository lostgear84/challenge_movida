"""Métricas de referência da Sprint 1."""
import re
from collections import Counter, defaultdict

from baseline import classificar

NUMERICAS = {"km", "tag_ocorrencia", "horario"}


def cobertura_taxonomia(taxonomia):
    nomes = {i["nome"] for i in taxonomia["intencoes"]}
    mapa = taxonomia["mapeamento_user_stories"]
    ok = [m for m in mapa if m["intencao"] in nomes]
    return {"stories": len(mapa), "mapeadas": len(ok), "cobertura": len(ok) / len(mapa)}


def acuracia_baseline(corpus):
    pred = [classificar(r["texto_normalizado"])[0] for r in corpus]
    ouro = [r["intencao"] for r in corpus]
    acertos = sum(p == o for p, o in zip(pred, ouro))
    por = defaultdict(lambda: [0, 0])
    for p, o in zip(pred, ouro):
        por[o][1] += 1
        por[o][0] += p == o
    erros = Counter((o, p) for p, o in zip(pred, ouro) if p != o)
    return {"acuracia": round(acertos / max(len(ouro), 1), 3), "acertos": acertos, "total": len(ouro),
            "por_intencao": {k: f"{a}/{t}" for k, (a, t) in sorted(por.items())},
            "confusoes_mais_comuns": erros.most_common(10)}


def taxa_normalizacao(corpus):
    """% das entidades numéricas anotadas cujo trecho no texto normalizado já está
    no formato canônico (dígitos), ou seja, que a normalização converteu."""
    total = conv = 0
    falhas = []
    for r in corpus:
        for e in r["entidades"]:
            if e["tipo"] not in NUMERICAS:
                continue
            total += 1
            trecho = r["texto_normalizado"][e["span"][0]:e["span"][1]]
            canon = (("%g" % e["valor"]) if e["tipo"] == "km" else str(e["valor"]))
            if re.search(rf"(?<![\d.]){re.escape(canon)}(?![\d.])", trecho):
                conv += 1
            else:
                falhas.append((r["id"], e["tipo"], trecho, canon))
    return {"entidades_numericas": total, "convertidas": conv,
            "taxa": round(conv / total, 3) if total else None, "falhas": falhas}
