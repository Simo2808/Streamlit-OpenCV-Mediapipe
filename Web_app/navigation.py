import streamlit as st
from urllib.parse import urlencode
import cv2

def switch_page(page_name):
    print("entro in navigation")
    print("nome pagina passata: "+page_name)
    params = urlencode({"page": page_name})
    st.query_params["page"] = page_name
    print("salvo la pagine nella query")
    st.rerun()