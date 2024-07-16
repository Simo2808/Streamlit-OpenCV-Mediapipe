import streamlit as st
import cv2
import numpy as np




def main():
    st.title("Webcam in tempo reale con OpenCV")
 # Inizializza la webcam


    cap = ChooseHandClass.getCap()

    # Crea un placeholder per il frame della webcam
    frame_placeholder = st.empty()

    # Pulsante per fermare la webcam
    stop_button = st.button("Ferma webcam")


    while not stop_button:
        frame = chooseHand.returnMain()
        if frame is not None:
            # Mostra il frame nel placeholder
            frame_placeholder.image(frame, channels="RGB")
        else:
            st.write("Impossibile accedere alla webcam")
            break

    # Rilascia la webcam
    cap.release()
