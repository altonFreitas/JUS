import streamlit as st

def dashboard():
    usuario = st.session_state.get('usuario', 'Utilizador')
    st.title(f"Bem-vindo ao Painel, {usuario}! 🚀")
    st.write("Este é o conteúdo protegido.")

    if st.button("Logout", use_container_width=True):
        st.session_state['pagina'] = 'Login'
        st.session_state.pop('usuario', None)
