import streamlit as st
from utils.storage import carregar_contas
from utils.classes import Conta

st.title("5 — Extratos e Relatórios")

contas_raw = carregar_contas()
contas = [Conta.from_dict(d) for d in contas_raw]

if not contas:
    st.info("Nenhuma conta cadastrada.")
else:
    sel = st.selectbox("Selecione conta para extrato", [f"{c.numero} - {c.titular_cpf_cnpj}" for c in contas])
    num = int(sel.split(" - ")[0])
    conta = next(c for c in contas if c.numero == num)

    st.write(f"**Conta {conta.numero}** — Titular: {conta.titular_cpf_cnpj} — Saldo: R$ {conta.saldo:.2f}")

    st.subheader("Movimentações (mais recentes primeiro)")
    if conta.movimentos:
        for m in reversed(conta.movimentos):
            st.write(f"- {m['timestamp']} — {m['descricao']} — R$ {m['valor']:.2f} — Saldo pós: R$ {m['saldo_pos']:.2f}")
    else:
        st.info("Sem movimentações.")

    # relatório simples
    st.subheader("Relatório resumido")
    total_depositos = sum(m["valor"] for m in conta.movimentos if m["valor"] > 0)
    total_saques = -sum(m["valor"] for m in conta.movimentos if m["valor"] < 0)
    st.write(f"Total de depósitos: R$ {total_depositos:.2f}")
    st.write(f"Total de saques: R$ {total_saques:.2f}")
