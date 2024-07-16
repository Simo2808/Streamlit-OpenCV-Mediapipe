import streamlit as st
from urllib.parse import urlencode
import navigation
import warnings

SET_MOD="complete"

# Filtra i warning
warnings.filterwarnings("ignore")

def main():
    
    col1, col2, col3 = st.columns([1, 10, 1])
    
    with col2:
        st.title('Prototipo Gesture Recognition')
    
    # Personalizzazione bottone
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    local_css('style.css')

    
    # Bottone per navigare alla pagina completa
    if st.button("COMPLETE VERSION", key='complete_version'):
        navigation.switch_page("complete")
    
    # Bottone per navigare alla pagina semplificata
    if st.button("SIMPLIFIED VERSION", key='simplified_version'):
        navigation.switch_page("simplified")

    

if __name__ == "__main__":
    print("sono entrato nella main page")
    page = st.query_params.get("page", "main")
    print(page)
    if page == "complete":
        SET_MOD = "complete"
        print("ho scelto complete")
        from gesture_recognizer import GestureRecognizer
        rec = GestureRecognizer()
        rec.main(1)
    
    elif page == "gesture_recognizer_right_semplified":
        from gesture_recognizer_right import GestureRecognizerRight
        rec = GestureRecognizerRight()
        rec.main(1)


    elif page == "simplified":
        SET_MOD = "semplified"
        from gesture_recognizer import GestureRecognizer
        rec = GestureRecognizer()
        rec.main(2)


    elif page == "gesture_recognizer_right_complete":
        from gesture_recognizer_right import GestureRecognizerRight
        rec = GestureRecognizerRight()
        rec.main(2)

    elif page == "gesture_recognizer_left_complete":
        from gesture_recognizer_left import GestureRecognizerLeft
        rec = GestureRecognizerLeft()
        rec.main(2)

    elif page == "gesture_recognizer_left_semplified":
        from gesture_recognizer_left import GestureRecognizerLeft
        rec = GestureRecognizerLeft()
        rec.main(1)

    else:
        main()