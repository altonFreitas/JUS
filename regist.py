import streamlit as st
from utils import carregar_usuarios, salvar_usuario, gerar_hash

def registrar():
    st.subheader("📅 Criar nova conta")
    novo_usuario = st.text_input("👤 Nome de utilizador")
    nova_senha = st.text_input("🔐 Senha", type="password")
    confirmar_senha = st.text_input("🔐 Confirmar senha", type="password")

    if st.button("Registrar", use_container_width=True):
        if novo_usuario and nova_senha and confirmar_senha:
            if nova_senha == confirmar_senha:
                usuarios = carregar_usuarios()
                if novo_usuario in usuarios:
                    st.error("Utilizador já existe. Escolha outro nome.")
                else:
                    senha_hash = gerar_hash(nova_senha)
                    salvar_usuario(novo_usuario, senha_hash)
                    st.success("🎉 Conta criada com sucesso! Faça login.")
                    st.session_state['pagina'] = 'Login'
            else:
                st.error("🔒 As senhas não coincidem.")
        else:
            st.error("🔒 Por favor, preencha todos os campos.")

    if st.button("Já tenho conta", use_container_width=True):
        st.session_state['pagina'] = 'Login'
 
