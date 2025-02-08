import streamlit as st
import hashlib
import pandas as pd
import os

# Definir a configuração da página como a primeira linha de código
st.set_page_config(page_title="JUS MENTOR ACADEMY", page_icon="🔐", layout="centered")

# Definir a página inicial
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'Login'

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

# Função para carregar ou inicializar o "fichário"
def carregar_dados():
    if 'fichario' not in st.session_state:
        st.session_state.fichario = pd.DataFrame(columns=["Título", "Descrição", "Link", "Arquivo"])
    return st.session_state.fichario

# Função para salvar os dados
def salvar_dados(df):
    st.session_state.fichario = df

# Função para salvar o arquivo no sistema
def salvar_arquivo(uploaded_file):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Função principal do aplicativo
def main():
    st.title("JUS MENTOR ACADEMY")

    # Estado para alternar entre as páginas
    if 'pagina' not in st.session_state:
        st.session_state.pagina = 'Login'

    if st.session_state.pagina == "Registrar":
        st.subheader("Criar nova conta")
        novo_usuario = st.text_input("👤 Nome de utilizador")
        nova_senha = st.text_input("🔐 Senha", type="password")
        confirmar_senha = st.text_input("🔐 Confirmar senha", type="password")

        if st.button("Registrar", use_container_width=True):
            if novo_usuario and nova_senha and confirmar_senha:
                if nova_senha == confirmar_senha:
                    usuarios = carregar_usuarios()
                    if novo_usuario in usuarios:
                        st.error("Usuário já existe. Escolha outro nome.")
                    else:
                        senha_hash = gerar_hash(nova_senha)
                        salvar_usuario(novo_usuario, senha_hash)
                        st.success("Conta criada com sucesso! Faça login.")
                        st.session_state.pagina = 'Login'
                        st.experimental_rerun()
                else:
                    st.error("🔒 As senhas não coincidem.")
            else:
                st.error("🔒 Por favor, preencha todos os campos.")

        if st.button("Já tenho conta", use_container_width=True):
            st.session_state.pagina = 'Login'

    elif st.session_state.pagina == "Login":
        usuario = st.text_input("👤 Nome de usuário")
        senha = st.text_input("🔐 Senha", type="password")

        if st.button("Login", use_container_width=True):
            if usuario and senha:
                usuarios = carregar_usuarios()
                if usuario in usuarios and usuarios[usuario] == gerar_hash(senha):
                    st.success(f"📢 Bem-vindo, {usuario}!")
                    st.session_state.usuario_logado = usuario
                    st.session_state.pagina = 'Dashboard'
                else:
                    st.error("🔒 Usuário ou senha incorretos.")
            else:
                st.error("🔒 Por favor, preencha todos os campos.")

        if st.button("Registrar conta", use_container_width=True):
            st.session_state.pagina = 'Registrar'

    elif st.session_state.pagina == "Dashboard":
        st.header(f"📚 Bem-vindo ao Dashboard, {st.session_state.usuario_logado}")
        fichario = carregar_dados()

        opcao = st.sidebar.selectbox("Escolha uma opção", ["Adicionar Material", "Visualizar Materiais", "Editar Material", "Excluir Material", "Logout"])

        if opcao == "Adicionar Material":
            st.header("Adicionar Novo Material")
            titulo = st.text_input("Título do Material")
            descricao = st.text_area("Descrição do Material")
            link = st.text_input("Link do Material (opcional)")
            uploaded_file = st.file_uploader("Carregar arquivo (PDF, etc.)", type=["pdf"])

            if st.button("Adicionar"):
                if titulo and descricao:
                    arquivo_path = None
                    if uploaded_file:
                        arquivo_path = salvar_arquivo(uploaded_file)

                    novo_material = pd.DataFrame([[titulo, descricao, link, arquivo_path]], columns=["Título", "Descrição", "Link", "Arquivo"])
                    fichario = pd.concat([fichario, novo_material], ignore_index=True)
                    salvar_dados(fichario)
                    st.success("Material adicionado com sucesso!")
                else:
                    st.error("Por favor, preencha o título e a descrição.")

        elif opcao == "Visualizar Materiais":
            st.header("Materiais Disponíveis")
            if not fichario.empty:
                for index, row in fichario.iterrows():
                    st.subheader(row["Título"])
                    st.write(row["Descrição"])
                    if row["Link"]:
                        st.markdown(f"[Acessar Link]({row['Link']})")
                    if row["Arquivo"]:
                        with open(row["Arquivo"], "rb") as f:
                            st.download_button(
                                label="Baixar Arquivo",
                                data=f,
                                file_name=os.path.basename(row["Arquivo"]),
                                mime="application/pdf"
                            )
                    st.write("---")
            else:
                st.info("Nenhum material cadastrado ainda.")

        elif opcao == "Editar Material":
            st.header("Editar Material Existente")
            if not fichario.empty:
                material_para_editar = st.selectbox("Selecione o material para editar", fichario["Título"].tolist())
                indice = fichario[fichario["Título"] == material_para_editar].index[0]

                novo_titulo = st.text_input("Novo Título", fichario.at[indice, "Título"])
                nova_descricao = st.text_area("Nova Descrição", fichario.at[indice, "Descrição"])
                novo_link = st.text_input("Novo Link", fichario.at[indice, "Link"])
                novo_arquivo = st.file_uploader("Carregar novo arquivo (PDF, etc.)", type=["pdf"])

                if st.button("Salvar Alterações"):
                    fichario.at[indice, "Título"] = novo_titulo
                    fichario.at[indice, "Descrição"] = nova_descricao
                    fichario.at[indice, "Link"] = novo_link
                    if novo_arquivo:
                        arquivo_path = salvar_arquivo(novo_arquivo)
                        fichario.at[indice, "Arquivo"] = arquivo_path
                    salvar_dados(fichario)
                    st.success("Material atualizado com sucesso!")
            else:
                st.info("Nenhum material cadastrado para editar.")

        elif opcao == "Excluir Material":
            st.header("Excluir Material")
            if not fichario.empty:
                material_para_excluir = st.selectbox("Selecione o material para excluir", fichario["Título"].tolist())
                if st.button("Excluir"):
                    arquivo_path = fichario[fichario["Título"] == material_para_excluir]["Arquivo"].values[0]
                    if arquivo_path and os.path.exists(arquivo_path):
                        os.remove(arquivo_path)

                    fichario = fichario[fichario["Título"] != material_para_excluir]
                    salvar_dados(fichario)
                    st.success("Material excluído com sucesso!")
            else:
                st.info("Nenhum material cadastrado para excluir.")

        elif opcao == "Logout":
            st.session_state.pagina = 'Login'
            st.success("Sessão terminada com sucesso!")
       

if __name__ == "__main__":
    main()
