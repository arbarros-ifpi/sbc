import streamlit as st

st.set_page_config(page_title="Sistema Bancário", layout="wide")
st.title("🏦 Sistema de Controle Bancário (Prototipagem)")
st.write("Use o menu lateral (páginas) para navegar pelo sistema.")
st.markdown("""
**Páginas disponíveis:**  
- 1. Clientes — cadastrar e listar clientes  
- 2. Funcionários — cadastrar e listar funcionários  
- 3. Contas — criar contas para clientes  
- 4. Movimentações — depósitos, saques, transferências, aplicar juros  
- 5. Extratos e Relatórios — ver movimentações  
- 6. Sobre — informações do sistema
""")
