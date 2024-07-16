import streamlit as st



def semplified_page():
    st.title("Semplified Version")
    st.write("Questa è la versione completa")

    # Bottone per tornare alla pagina principale
    if st.button("Back to Main Page"):
        from navigation import switch_page
        switch_page("main")