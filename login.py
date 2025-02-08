import streamlit as st

# Função para simular um banco de dados de usuários
usuarios = {}

def registrar_usuario(email, senha):
    if email in usuarios:
        return False  # Usuário já existe
    usuarios[email] = senha
    return True

def verificar_login(email, senha):
    if email in usuarios and usuarios[email] == senha:
        return True  # Login válido
    return False  # Login inválido

# Interface do Streamlit
st.title("Sistema de Login e Registro")

# Menu de escolha (Login ou Registro)
menu = st.selectbox("Escolha uma opção", ["Login", "Registro"])

if menu == "Registro":
    st.subheader("Criar nova conta")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    confirmar_senha = st.text_input("Confirmar Senha", type="password")

    if st.button("Registrar"):
        if senha == confirmar_senha:
            if registrar_usuario(email, senha):
                st.success("Conta criada com sucesso!")
            else:
                st.error("Este email já está registrado.")
        else:
            st.error("As senhas não coincidem.")

elif menu == "Login":
    st.subheader("Faça login")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Login"):
        if verificar_login(email, senha):
            st.success(f"Bem-vindo, {email}!")
        else:
            st.error("Email ou senha incorretos.")