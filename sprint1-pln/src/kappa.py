"""Concordância entre anotadores (Cohen's kappa)."""
from collections import Counter


def cohen_kappa(a, b):
    """kappa = (po - pe) / (1 - pe). a e b: listas de rótulos, mesma ordem."""
    assert len(a) == len(b) and a, "listas vazias ou de tamanhos diferentes"
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[r] * cb[r] for r in set(ca) | set(cb)) / (n * n)
    if pe == 1:
        return 1.0
    return (po - pe) / (1 - pe)


def kappa_por_intencao(a, b):
    """Kappa binário (a intenção X vs. todo o resto) para cada intenção."""
    rotulos = sorted(set(a) | set(b))
    res = {}
    for r in rotulos:
        xa = [x == r for x in a]
        xb = [y == r for y in b]
        res[r] = {"kappa": round(cohen_kappa(xa, xb), 3),
                  "n_a1": sum(xa), "n_a2": sum(xb)}
    return res


def gate(a, b, limiar=0.70):
    geral = cohen_kappa(a, b)
    por = kappa_por_intencao(a, b)
    abaixo = {k: v for k, v in por.items() if v["kappa"] < limiar}
    return {"kappa_geral": round(geral, 3), "limiar": limiar, "passa_geral": geral >= limiar,
            "intencoes_abaixo_do_limiar": abaixo, "por_intencao": por}
