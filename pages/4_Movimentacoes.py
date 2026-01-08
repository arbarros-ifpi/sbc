import streamlit as st
from utils.storage import carregar_contas, salvar_contas
from utils.classes import Conta

st.title("4 — Movimentações")

contas_raw = carregar_contas()
if "contas" not in st.session_state:
    st.session_state["contas"] = [Conta.from_dict(d) for d in contas_raw]

contas = st.session_state["contas"]

if not contas:
    st.warning("Cadastre contas primeiro.")
else:
    sel = st.selectbox("Selecione a conta", [f"{c.numero} - {c.titular_cpf_cnpj} ({c.tipo})" for c in contas])
    numero_sel = int(sel.split(" - ")[0])
    conta = next(c for c in contas if c.numero == numero_sel)

    oper = st.selectbox("Operação", ["Depósito", "Saque", "Transferência", "Aplicar Juros (poupança)"])
    valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0)
    if oper == "Transferência":
        destino_sel = st.selectbox("Conta destino", [f"{c.numero} - {c.titular_cpf_cnpj}" for c in contas if c.numero != conta.numero])
    if st.button("Executar"):
        if oper == "Depósito":
            conta.depositar(valor)
            st.success(f"Depósito de R$ {valor:.2f} realizado.")
        elif oper == "Saque":
            if conta._pode_sacar(valor):
                conta.sacar(valor)
                st.success(f"Saque de R$ {valor:.2f} realizado.")
            else:
                st.error("Saque negado — saldo/limite insuficiente.")
        elif oper == "Transferência":
            num_dest = int(destino_sel.split(" - ")[0])
            destino = next(c for c in contas if c.numero == num_dest)
            if conta.transferir_para(destino, valor):
                st.success(f"Transferência de R$ {valor:.2f} para conta {destino.numero} efetuada.")
            else:
                st.error("Transferência negada — saldo/limite insuficiente.")
        elif oper == "Aplicar Juros (poupança)":
            juros = conta.aplicar_juros()
            if juros > 0:
                st.success(f"Juros aplicados: R$ {juros:.2f}")
            else:
                st.warning("Operação válida apenas para contas poupança.")

        # salva alterações
        salvar_contas([c.to_dict() for c in contas])

    st.info(f"Saldo atual: R$ {conta.saldo:.2f}")
    st.subheader("Últimas movimentações")
    if conta.movimentos:
        for m in reversed(conta.movimentos[-10:]):
            st.write(f"{m['timestamp']} — {m['descricao']} — R$ {m['valor']:.2f} — Saldo: R$ {m['saldo_pos']:.2f}")
    else:
        st.info("Sem movimentações.")
