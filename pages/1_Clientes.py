import streamlit as st
from utils.classes import Pessoa
from utils.storage import carregar_pessoas, salvar_pessoas

st.title("1 — Cadastro de Clientes")

# carrega dados (lista de dicts)
pessoas_raw = carregar_pessoas()

# session_state para não recarregar
if "pessoas" not in st.session_state:
    st.session_state["pessoas"] = [Pessoa.from_dict(d) for d in pessoas_raw]

with st.form("form_cad_cliente", clear_on_submit=True):
    nome = st.text_input("Nome completo")
    tipo = st.selectbox("Tipo", ["Física", "Jurídica"])
    cpf_cnpj = st.text_input("CPF / CNPJ")
    email = st.text_input("Email")
    enviar = st.form_submit_button("Cadastrar")

if enviar:
    if not nome.strip() or not cpf_cnpj.strip():
        st.error("Informe nome e CPF/CNPJ.")
    else:
        # checa duplicidade
        existe = any(p.cpf_cnpj == cpf_cnpj for p in st.session_state["pessoas"])
        if existe:
            st.error("Já existe cliente com esse CPF/CNPJ.")
        else:
            novo = Pessoa(nome=nome.strip(), tipo=tipo, cpf_cnpj=cpf_cnpj.strip(), email=email.strip())
            st.session_state["pessoas"].append(novo)
            # salva em arquivo (converter para dict)
            salvar_pessoas([p.to_dict() for p in st.session_state["pessoas"]])
            st.success(f"Cliente '{nome}' cadastrado com sucesso!")

st.subheader("Clientes cadastrados")
if st.session_state["pessoas"]:
    for p in st.session_state["pessoas"]:
        st.write(f"- **{p.nome}** — {p.tipo} — {p.cpf_cnpj} — {p.email}")
else:
    st.info("Nenhum cliente cadastrado.")
