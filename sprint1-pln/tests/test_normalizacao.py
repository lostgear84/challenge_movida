import sys, pathlib
RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from normalizacao import Normalizador, localizar_span

N = Normalizador(RAIZ / "glossario_rodoviario.json")

CASOS = [
    ("registra aí uma ocorrencia no km cento e vinte e tres e meio sentido capital",
     "registrar uma ocorrência no km 123.5 sentido capital"),
    ("Informa que tem óleo na pista no km cinquenta e um mais trezentos, sentido capital.",
     "informar que tem óleo na pista no km 51.3 sentido capital"),
    ("Guincho chegando no local da ocorrência três quatro sete, previsão de cinco minutos.",
     "guincho chegando no local da ocorrência 347 previsão de 5 minutos"),
    ("Finaliza a missão, via liberada às quinze e quarenta.",
     "finalizar a missão via liberada às 15:40"),
    ("Ó, tô no km oitenta e sete sentido interior, acidente com dois carros, faixa dois bloqueada.",
     "tô no km 87 sentido interior acidente com 2 carros faixa 2 bloqueada"),
    ("Hã... registra no quilômetro duzentos e quatro", "registrar no km 204"),
    ("KM 123,5 sentido litoral", "km 123.5 sentido litoral"),
    ("km 51+300", "km 51.3"),
    ("faixa um", "faixa 1"),
    ("mais uma viatura", "mais uma viatura"),
    ("dois mil e vinte e seis", "2026"),
    ("ocorrência três meia sete", "ocorrência 367"),
    ("pressão doze por oito", "pressão 12 por 8"),
    ("às duas horas", "às 02:00"),
    ("é... cheguei no local", "cheguei no local"),
    ("Quilômetro de cento e quarenta e três e meio", "km 143.5"),
    ("São 14,32 do momento", "são 14:32 do momento"),
]

def test_casos():
    falhas = []
    for entrada, esperado in CASOS:
        obtido = N.normalizar(entrada)
        if obtido != esperado:
            falhas.append((entrada, esperado, obtido))
    assert not falhas, "\n".join(f"{e!r}\n  esperado {s!r}\n  obtido   {o!r}" for e, s, o in falhas)

def test_span():
    t = "registrar uma ocorrência no km 123.5 sentido capital"
    s = localizar_span(t, "km 123.5")
    assert t[s[0]:s[1]] == "km 123.5"

if __name__ == "__main__":
    test_casos(); test_span(); print("ok")
