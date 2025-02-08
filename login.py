import streamlit as st
from utils import carregar_usuarios, gerar_hash

def login():
    st.subheader("🔓 Fazer login")
    usuario = st.text_input("👤 Nome de utilizador")
    senha = st.text_input("🔐 Senha", type="password")

    if st.button("Login", use_container_width=True):
        if usuario and senha:
            usuarios = carregar_usuarios()
            if usuario in usuarios and usuarios[usuario] == gerar_hash(senha):
                st.success(f"📢 Bem-vindo, {usuario}!")
                st.session_state['usuario'] = usuario
                st.session_state['pagina'] = 'Dashboard'
                st.experimental_rerun() 
            else:
                st.error("🔒 Utilizador ou senha incorretos.")
        else:
            st.error("🔒 Por favor, preencha todos os campos.")

    if st.button("Registrar conta", use_container_width=True):
        st.session_state['pagina'] = 'Registrar'
        st.experimental_rerun() 
