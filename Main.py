import streamlit as st
import pandas as pd
import os

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

# Interface do Streamlit
st.title("📚 JUS MENTOR ACADEMY TEST")
st.write("Bem-vindo ao sistema de gestão de materiais de aprendizagem!")

# Carregar dados
fichario = carregar_dados()

# Menu de opções
opcao = st.sidebar.selectbox("Escolha uma opção", ["Adicionar Material", "Visualizar Materiais", "Editar Material", "Excluir Material"])

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
            # Remove o arquivo físico associado, se existir
            arquivo_path = fichario[fichario["Título"] == material_para_excluir]["Arquivo"].values[0]
            if arquivo_path and os.path.exists(arquivo_path):
                os.remove(arquivo_path)
            
            # Remove o material do DataFrame
            fichario = fichario[fichario["Título"] != material_para_excluir]
            salvar_dados(fichario)
            st.success("Material excluído com sucesso!")
    else:
        st.info("Nenhum material cadastrado para excluir.")

# Exibir o estado atual do fichário (para debug)
st.sidebar.write("Estado atual do fichário:")
st.sidebar.write(fichario)