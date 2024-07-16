import cv2
import mediapipe as mp
from mediapipe.tasks import python
import threading 
from google.protobuf.json_format import MessageToDict 
import streamlit as st
import os    

HAND='Left'

st.cache_resource.clear()

class GestureRecognizerRight:


    def __init__(self):
        self.lock = threading.Lock()
        self.current_gestures = []    


    
    def main(self, mod):

        try:
        
            if mod == 2:
                st.title("Complete - Right version")
            elif mod == 1:
                st.title("Semplified - Right version")

            else:
                print("error!")
            
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            frame_placeholder = st.empty()

            """Main function to run the gesture recognition"""
            num_hands = 1



            ####### MENU - momentaneamente da terminale ############### --> messo nel main --> da eliminare qui

            print("(Sono entrato in questo file)Seleziona la modalità che si desidera utilizzare:")
            print("-SEMPLIFICATA 1")
            print("-COMPLETA 2")
            

            # Potremmo pensare ad un'idea di calibrazione dei comandi - di volta in volta arricchire il modello con immagini dell'utente (possibili problemi di privacy? - introduzione di un "termini e condizioni")

            print(mod)
            if (mod == 1):
                model = "gesture_recognizer_semplified_right.task"
            elif (mod == 2):
                model = "gesture_recognizer_complete_right.task"
            else:
                print("scelta non valida")
                exit(1)
            ##########################################################
          

            model_path = model
            GestureRecognizer = mp.tasks.vision.GestureRecognizer
            GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
            VisionRunningMode = mp.tasks.vision.RunningMode

            self.lock = threading.Lock() 
            self.current_gestures = [] 

            base_options_ = mp.tasks.BaseOptions(model_asset_buffer=open(model_path, "rb").read())

            options = GestureRecognizerOptions(
                base_options=base_options_,
                running_mode=VisionRunningMode.LIVE_STREAM,
                num_hands = num_hands,
                result_callback=self.__result_callback)
            recognizer = GestureRecognizer.create_from_options(options)

            timestamp = 0 
            mp_drawing = mp.solutions.drawing_utils
            mp_hands = mp.solutions.hands

            hands = mp_hands.Hands(
                    static_image_mode=False,
                    max_num_hands=num_hands,
                    min_detection_confidence=0.65,
                    min_tracking_confidence=0.65)



            #variabili gestione iniziale

            flag_hand_left_or_right = 0
            previous_hand_recognized = ""
            count_frame_hand_recognized = 0

            stop_button = st.button("Ferma webcam")

            #a loop for the gesture recognition per frame
            while not stop_button:
                ret, frame = cap.read()
                if not ret:
                    st.write("Impossibile accedere alla fotocamera")
                    cap.release()
                    break

                

                #provo ad inserire qui il loop per la visione del testo che avvisa la corretta registrazione della mano
                

                #converting the frame to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                #processing the frame to detect hands and landmarks
                results = hands.process(frame)
                
                #flip frame
                #frame = cv2.flip(frame,1)

                #converting frame back to BGR for rendering
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                np_array = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                #code to recognize gestures if hands are detected
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        #drawing hand landmarks on the frame

                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(0, 139, 69), thickness=1, circle_radius=3))
                        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np_array)
                        recognizer.recognize_async(mp_image, timestamp)
                        timestamp = timestamp + 1 
                    else: # l'intero else messo nel main --> da rimuovere qui
                        
                        for i in results.multi_handedness:
                        # hand/left recognition

                            label = MessageToDict(i)[   # ---> in results.multi_handedness ho tutte le informazioni della mano in formato protobuf. con il metodo MessageToDict trasformo l'informazione in questo formato in un dizionario (facilito l'accesso alle informazioni). Accedo dunque alla sezione 'classification' -> posizione '0' -> contenuto 'label' (che contiene l'informazione sulla tipologia della mano mostrata)
                            'classification'][0]['label'] 

    
                            #eventualmente ricontrollare qui !!!
                            if (label != HAND):
                                    cv2.putText(frame, "Error! You're showing the wrong hand!", (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)


                            #controllo mantenimento posizione per un tempo sufficiente
                            if previous_hand_recognized == label and flag_hand_left_or_right == 0:
                                    count_frame_hand_recognized += 1
                            else: 
                                count_frame_hand_recognized = 0

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.put_gestures(frame)
                frame_placeholder.image(frame, channels="RGB")
                   

        finally:
            if cap is not None:
                 cap.release()
            #if GestureRecognizer is not None:
                    #GestureRecognizer.close()
            cv2.destroyAllWindows()
                

        
        #cv2.imshow('Gesture Recognition using Mediapipe', frame)
               
        
            
        if stop_button:
            if cap is not None:
                cap.release()
                #if GestureRecognizer is not None:
                    #GestureRecognizer.close()
            #cv2.destroyAllWindows()
            from navigation import switch_page
            switch_page("main")

 


    def put_gestures(self, frame):
        """Puts the name of the recognized gestures on the frame"""
        self.lock.acquire()
        gestures = self.current_gestures
        self.lock.release()
        y_pos = 50
        for hand_gesture_name in gestures:
            cv2.putText(frame, hand_gesture_name, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (255,255,255), 2, cv2.LINE_AA)
            y_pos += 50

    def __result_callback(self, result, output_image, timestamp_ms):
        """Callback function to get the result of the gesture recognition"""
        #print(f'gesture recognition result: {result}')  #prints the whole result 
        self.lock.acquire() 
        self.current_gestures = []
        if result is not None and any(result.gestures):
            print("Recognized gestures:")
            for single_hand_gesture_data in result.gestures:
                gesture_name = single_hand_gesture_data[0].category_name
                self.current_gestures.append(gesture_name)
        self.lock.release()

