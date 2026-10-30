"""Validação do corpus contra o contrato de saída (JSON Schema montado a partir
da taxonomia e do esquema de entidades — uma única fonte de verdade)."""
import json
from pathlib import Path
from jsonschema import Draft7Validator


def montar_schema(taxonomia, esquema_entidades):
    intencoes = [i["nome"] for i in taxonomia["intencoes"]]
    personas = list(taxonomia["personas"].keys())
    tipos = [t["tipo"] for t in esquema_entidades["tipos"]]
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "corpus_enunciacoes",
        "type": "array",
        "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["id", "persona", "transcricao_bruta", "texto_normalizado", "intencao",
                         "entidades", "exige_confirmacao", "anotadores", "concordancia"],
            "properties": {
                "id": {"type": "string", "pattern": "^enu_\\d{4}$"},
                "persona": {"enum": personas},
                "transcricao_bruta": {"type": "string", "minLength": 1},
                "texto_normalizado": {"type": "string", "minLength": 1},
                "intencao": {"enum": intencoes},
                "entidades": {"type": "array", "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["tipo", "valor", "span"],
                    "properties": {
                        "tipo": {"enum": tipos},
                        "valor": {"type": ["number", "string"]},
                        "span": {"type": "array", "items": {"type": "integer", "minimum": 0},
                                 "minItems": 2, "maxItems": 2}}}},
                "exige_confirmacao": {"type": "boolean"},
                "anotadores": {"type": "array", "items": {"type": "string"}, "minItems": 2},
                "concordancia": {"type": "number", "minimum": 0, "maximum": 1},
            },
        },
    }


def validar(corpus, taxonomia, esquema_entidades):
    """Retorna lista de erros (vazia = tudo válido). Além do schema, checa
    regras que JSON Schema não expressa."""
    schema = montar_schema(taxonomia, esquema_entidades)
    erros = [f"{list(e.path)}: {e.message}" for e in Draft7Validator(schema).iter_errors(corpus)]
    tax = {i["nome"]: i for i in taxonomia["intencoes"]}
    ids = [r.get("id") for r in corpus]
    if len(ids) != len(set(ids)):
        erros.append("ids repetidos")
    for r in corpus:
        t = r.get("texto_normalizado", "")
        for e in r.get("entidades", []):
            a, b = e["span"]
            if not (0 <= a < b <= len(t)):
                erros.append(f"{r['id']}: span {e['span']} fora do texto")
        i = tax.get(r.get("intencao"))
        if i and r.get("exige_confirmacao") != i["exige_confirmacao"]:
            erros.append(f"{r['id']}: exige_confirmacao diferente da taxonomia")
    return erros


def avisos_permissao(corpus, taxonomia):
    """Enunciações de persona sem permissão para a intenção (não é erro de schema,
    é sinal para a governança: o agente deveria recusar)."""
    perm = {i["nome"]: i["personas_autorizadas"] for i in taxonomia["intencoes"]}
    return [r["id"] for r in corpus if r["persona"] not in perm.get(r["intencao"], [])]


def salvar_schema(taxonomia, esquema_entidades, caminho):
    Path(caminho).write_text(json.dumps(montar_schema(taxonomia, esquema_entidades),
                                        ensure_ascii=False, indent=2), encoding="utf-8")
