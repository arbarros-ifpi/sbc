from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Pessoa:
    nome: str
    tipo: str   # "Física" ou "Jurídica"
    cpf_cnpj: str = ""
    email: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "cpf_cnpj": self.cpf_cnpj,
            "email": self.email
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Pessoa":
        return Pessoa(
            nome=d.get("nome", ""),
            tipo=d.get("tipo", ""),
            cpf_cnpj=d.get("cpf_cnpj", ""),
            email=d.get("email", "")
        )

@dataclass
class Funcionario:
    nome: str
    cargo: str
    id_func: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nome": self.nome,
            "cargo": self.cargo,
            "id_func": self.id_func
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Funcionario":
        return Funcionario(
            nome=d.get("nome", ""),
            cargo=d.get("cargo", ""),
            id_func=d.get("id_func", "")
        )

@dataclass
class Conta:
    numero: int
    titular_cpf_cnpj: str
    tipo: str  # 'corrente', 'poupanca', 'especial'
    saldo: float = 0.0
    limite: float = 0.0
    movimentos: List[Dict[str, Any]] = field(default_factory=list)

    def depositar(self, valor: float):
        self.saldo += valor
        self.registrar("Depósito", valor)

    def sacar(self, valor: float) -> bool:
        if valor <= self.saldo:
            self.saldo -= valor
            self.registrar("Saque", -valor)
            return True
        return False

    def transferir_para(self, destino: "Conta", valor: float) -> bool:
        # usa regras de saque da conta
        if self._pode_sacar(valor):
            self.saldo -= valor
            destino.saldo += valor
            self.registrar(f"Transferência para {destino.numero}", -valor)
            destino.registrar(f"Transferência de {self.numero}", valor)
            return True
        return False

    def registrar(self, descricao: str, valor: float):
        from datetime import datetime
        self.movimentos.append({
            "descricao": descricao,
            "valor": valor,
            "saldo_pos": round(self.saldo, 2),
            "timestamp": datetime.now().isoformat()
        })

    def _pode_sacar(self, valor: float) -> bool:
        # padrão: somente saldo disponível
        return valor <= self.saldo

    def aplicar_juros(self):
        # somente poupança: 1% ao mês
        if self.tipo == "poupanca":
            juros = round(self.saldo * 0.01, 2)
            self.saldo += juros
            self.registrar("Rendimento 1%", juros)
            return juros
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "numero": self.numero,
            "titular_cpf_cnpj": self.titular_cpf_cnpj,
            "tipo": self.tipo,
            "saldo": self.saldo,
            "limite": self.limite,
            "movimentos": self.movimentos
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Conta":
        c = Conta(
            numero=d.get("numero", 0),
            titular_cpf_cnpj=d.get("titular_cpf_cnpj", ""),
            tipo=d.get("tipo", "corrente"),
            saldo=d.get("saldo", 0.0),
            limite=d.get("limite", 0.0),
            movimentos=d.get("movimentos", [])
        )
        return c
