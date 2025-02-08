import streamlit as st
import os

# Pasta para armazenar os vídeos
PASTA_VIDEOS = "videos"
if not os.path.exists(PASTA_VIDEOS):
    os.makedirs(PASTA_VIDEOS)

# Função para listar vídeos
def listar_videos():
    return [f for f in os.listdir(PASTA_VIDEOS) if f.endswith((".mp4", ".avi", ".mkv"))]

# Função para adicionar um vídeo
def adicionar_video(arquivo):
    caminho_video = os.path.join(PASTA_VIDEOS, arquivo.name)
    with open(caminho_video, "wb") as f:
        f.write(arquivo.getbuffer())
    st.success(f"Vídeo '{arquivo.name}' adicionado com sucesso!")

# Função para deletar um vídeo
def deletar_video(nome_arquivo):
    caminho_video = os.path.join(PASTA_VIDEOS, nome_arquivo)
    os.remove(caminho_video)
    st.success(f"Vídeo '{nome_arquivo}' deletado com sucesso!")

# Interface do Streamlit
st.title("CRUD de Vídeos")

# Menu de opções
opcao = st.sidebar.selectbox("Escolha uma opção", ["Adicionar Vídeo", "Ver Vídeos", "Deletar Vídeo"])

# Adicionar Vídeo
if opcao == "Adicionar Vídeo":
    st.subheader("Adicionar Vídeo")
    arquivo = st.file_uploader("Escolha um vídeo", type=["mp4", "avi", "mkv"])
    if arquivo is not None:
        if st.button("Adicionar"):
            adicionar_video(arquivo)

# Ver Vídeos
elif opcao == "Ver Vídeos":
    st.subheader("Vídeos Disponíveis")
    videos = listar_videos()
    if videos:
        for video in videos:
            caminho_video = os.path.join(PASTA_VIDEOS, video)
            st.write(f"Exibindo: {video}")
            st.video(caminho_video)  # Exibe o vídeo
    else:
        st.write("Nenhum vídeo disponível.")

# Deletar Vídeo
elif opcao == "Deletar Vídeo":
    st.subheader("Deletar Vídeo")
    videos = listar_videos()
    if videos:
        video_selecionado = st.selectbox("Escolha um vídeo para deletar", videos)
        if st.button("Deletar"):
            deletar_video(video_selecionado)
    else:
        st.write("Nenhum vídeo disponível para deletar.")