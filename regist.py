import streamlit as st
import hashlib

# Função para carregar usuários do ficheiro .txt
def carregar_usuarios():
    try:
        with open("usuarios.txt", "r") as file:
            usuarios = {}
            for linha in file:
                usuario, senha_hash = linha.strip().split(":")
                usuarios[usuario] = senha_hash
            return usuarios
    except FileNotFoundError:
        return {}

# Função para salvar usuários no ficheiro .txt
def salvar_usuario(usuario, senha_hash):
    with open("usuarios.txt", "a") as file:
        file.write(f"{usuario}:{senha_hash}\n")

# Função para gerar hash da senha (usando SHA-256)
def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Interface do Streamlit
st.title("🔐 Sistema de Registro e Login")

# Menu de opções
opcao = st.sidebar.selectbox("Escolha uma opção", ["Registrar", "Login"])

if opcao == "Registrar":
    st.header("Registrar Nova Conta")
    novo_usuario = st.text_input("Escolha um nome de usuário")
    nova_senha = st.text_input("Escolha uma senha", type="password")
    confirmar_senha = st.text_input("Confirme a senha", type="password")

    if st.button("Registrar"):
        if novo_usuario and nova_senha and confirmar_senha:
            if nova_senha == confirmar_senha:
                usuarios = carregar_usuarios()
                if novo_usuario in usuarios:
                    st.error("Usuário já existe. Escolha outro nome.")
                else:
                    senha_hash = gerar_hash(nova_senha)
                    salvar_usuario(novo_usuario, senha_hash)
                    st.success("Conta criada com sucesso! Faça login.")
            else:
                st.error("As senhas não coincidem.")
        else:
            st.error("Por favor, preencha todos os campos.")

elif opcao == "Login":
    st.header("Login")
    usuario = st.text_input("Nome de usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Login"):
        if usuario and senha:
            usuarios = carregar_usuarios()
            if usuario in usuarios and usuarios[usuario] == gerar_hash(senha):
                st.success("Login bem-sucedido!")
                st.write(f"Bem-vindo, {usuario}!")
                # Redirecionar para outra página (substitua pelo seu código)
                # st.experimental_rerun()  # Para recarregar a página
            else:
                st.error("Usuário ou senha incorretos.")
        else:
            st.error("Por favor, preencha todos os campos.")