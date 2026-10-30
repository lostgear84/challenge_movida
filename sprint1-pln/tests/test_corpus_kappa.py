"""Testes com dados SINTÉTICOS mínimos (não são o corpus)."""
import json, sys, pathlib
RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from kappa import cohen_kappa, gate
from corpus import montar_corpus
from validacao import validar
from metricas import cobertura_taxonomia, taxa_normalizacao, acuracia_baseline
from sklearn.metrics import cohen_kappa_score

TAX = json.loads((RAIZ / "taxonomia_intencoes.json").read_text(encoding="utf-8"))
ENT = json.loads((RAIZ / "dados/esquema_entidades.json").read_text(encoding="utf-8"))

def test_kappa_igual_sklearn():
    a = ["x", "x", "y", "z", "y", "x", "z", "z"]
    b = ["x", "y", "y", "z", "y", "x", "x", "z"]
    assert abs(cohen_kappa(a, b) - cohen_kappa_score(a, b)) < 1e-9
    assert cohen_kappa(a, a) == 1.0

def test_gate_detecta_intencao_fraca():
    a = ["p", "p", "q", "q", "r", "r"]
    b = ["p", "p", "q", "r", "q", "r"]
    g = gate(a, b)
    assert "q" in g["intencoes_abaixo_do_limiar"] and "p" not in g["intencoes_abaixo_do_limiar"]

def test_corpus_valido():
    tr = [{"id": "enu_0001", "transcricao_bruta": "registra aí uma ocorrencia no km cento e vinte e tres e meio sentido capital",
           "texto_normalizado": "registrar uma ocorrência no km 123.5 sentido capital"},
          {"id": "enu_0002", "transcricao_bruta": "cheguei no local", "texto_normalizado": "cheguei no local"}]
    pers = {"enu_0001": "inspecao_trafego", "enu_0002": "guincho"}
    a1 = [{"id": "enu_0001", "intencao": "registrar_ocorrencia", "entidades": "km=123.5@km 123.5; sentido=capital@sentido capital"},
          {"id": "enu_0002", "intencao": "atualizar_status", "entidades": "status=no_local@cheguei"}]
    a2 = [{"id": "enu_0001", "intencao": "registrar_ocorrencia", "entidades": "km=123.5@km 123.5"},
          {"id": "enu_0002", "intencao": "encerrar_atendimento", "entidades": ""}]
    corpus, pend = montar_corpus(tr, pers, a1, a2, None, TAX)
    assert len(corpus) == 1 and pend[0][0] == "enu_0002"
    assert corpus[0]["exige_confirmacao"] is True
    assert validar(corpus, TAX, ENT) == []
    assert taxa_normalizacao(corpus)["taxa"] == 1.0
    assert acuracia_baseline(corpus)["acuracia"] == 1.0
    ruim = [dict(corpus[0], intencao="inexistente")]
    assert validar(ruim, TAX, ENT)

def test_cobertura_100():
    assert cobertura_taxonomia(TAX)["cobertura"] == 1.0

if __name__ == "__main__":
    for f in [test_kappa_igual_sklearn, test_gate_detecta_intencao_fraca, test_corpus_valido, test_cobertura_100]:
        f()
    print("ok")
