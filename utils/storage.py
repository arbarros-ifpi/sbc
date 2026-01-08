import json
import os
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

PESSOAS_FILE = os.path.join(DATA_DIR, "pessoas.json")
FUNCIONARIOS_FILE = os.path.join(DATA_DIR, "funcionarios.json")
CONTAS_FILE = os.path.join(DATA_DIR, "contas.json")

def _read_json(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def _write_json(path: str, data: List[Dict[str, Any]]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Pessoas
def carregar_pessoas() -> List[Dict[str, Any]]:
    return _read_json(PESSOAS_FILE)

def salvar_pessoas(lista: List[Dict[str, Any]]):
    _write_json(PESSOAS_FILE, lista)

# Funcionários
def carregar_funcionarios() -> List[Dict[str, Any]]:
    return _read_json(FUNCIONARIOS_FILE)

def salvar_funcionarios(lista: List[Dict[str, Any]]):
    _write_json(FUNCIONARIOS_FILE, lista)

# Contas
def carregar_contas() -> List[Dict[str, Any]]:
    return _read_json(CONTAS_FILE)

def salvar_contas(lista: List[Dict[str, Any]]):
    _write_json(CONTAS_FILE, lista)
