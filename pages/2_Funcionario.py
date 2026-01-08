import streamlit as st
from utils.classes import Funcionario
from utils.storage import carregar_funcionarios, salvar_funcionarios

st.title("2 — Cadastro de Funcionários")

funcs_raw = carregar_funcionarios()
if "funcionarios" not in st.session_state:
    st.session_state["funcionarios"] = [Funcionario.from_dict(d) for d in funcs_raw]

with st.form("form_cad_func", clear_on_submit=True):
    nome = st.text_input("Nome completo")
    cargo = st.text_input("Cargo")
    id_func = st.text_input("ID do funcionário (opcional)")
    enviar = st.form_submit_button("Cadastrar funcionário")

if enviar:
    if not nome.strip() or not cargo.strip():
        st.error("Informe nome e cargo.")
    else:
        novo = Funcionario(nome=nome.strip(), cargo=cargo.strip(), id_func=id_func.strip())
        st.session_state["funcionarios"].append(novo)
        salvar_funcionarios([f.to_dict() for f in st.session_state["funcionarios"]])
        st.success(f"Funcionário '{nome}' cadastrado.")

st.subheader("Funcionários cadastrados")
if st.session_state["funcionarios"]:
    for f in st.session_state["funcionarios"]:
        st.write(f"- **{f.nome}** — {f.cargo} — {f.id_func}")
else:
    st.info("Nenhum funcionário cadastrado.")
