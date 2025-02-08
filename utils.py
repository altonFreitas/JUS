import hashlib

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

def salvar_usuario(usuario, senha_hash):
    with open("usuarios.txt", "a") as file:
        file.write(f"{usuario}:{senha_hash}\n")

def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()
