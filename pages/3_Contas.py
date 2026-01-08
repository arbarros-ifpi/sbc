import streamlit as st
from utils.classes import Pessoa, Conta,ContaCorrente,ContaPoupanca,ContaEspecial
from utils.storage import carregar_pessoas, carregar_contas, salvar_contas

st.title("3 — Cadastro de Contas")

# carrega clientes e contas de disco
pessoas_raw = carregar_pessoas()
contas_raw = carregar_contas()

if "pessoas" not in st.session_state:
    st.session_state["pessoas"] = [Pessoa.from_dict(d) for d in pessoas_raw]

if "contas" not in st.session_state:
    st.session_state["contas"] = [Conta.from_dict(d) for d in contas_raw]

pessoas = st.session_state["pessoas"]
contas = st.session_state["contas"]

if not pessoas:
    st.warning("Cadastre clientes antes de criar contas.")
else:
    cpf_list = [p.cpf_cnpj for p in pessoas]
    titular = st.selectbox("Titular (CPF/CNPJ)", cpf_list)
    tipo_conta = st.selectbox("Tipo de conta", ["corrente", "poupanca", "especial"])
    saldo_inicial = st.number_input("Saldo inicial (R$)", min_value=0.0, value=0.0, step=10.0)

    if st.button("Criar conta"):
        # determinar próximo número
        prox_num = 1
        if contas:
            prox_num = max(c.numero for c in contas) + 1

        if tipo_conta == "corrente":
            nova = ContaCorrente(prox_num, titular, saldo=saldo_inicial)
        elif tipo_conta == "poupanca":
            nova = ContaPoupanca(prox_num, titular, saldo=saldo_inicial)
        else:
            nova = ContaEspecial(prox_num, titular, saldo=saldo_inicial)

        st.session_state["contas"].append(nova)
        # salva
        salvar_contas([c.to_dict() for c in st.session_state["contas"]])
        st.success(f"Conta {nova.numero} ({nova.tipo}) criada para {titular}.")

st.subheader("Contas existentes")
if contas:
    for c in contas:
        st.write(f"- **Conta {c.numero}** — Titular: {c.titular_cpf_cnpj} — Tipo: {c.tipo} — Saldo: R$ {c.saldo:.2f}")
else:
    st.info("Nenhuma conta cadastrada.")
