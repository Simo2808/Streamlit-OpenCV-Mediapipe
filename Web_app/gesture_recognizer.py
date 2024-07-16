import cv2
import mediapipe as mp
from mediapipe.tasks import python
import threading 
from google.protobuf.json_format import MessageToDict 
import streamlit as st
import os    

st.cache_resource.clear()

class GestureRecognizer:

    def __init__(self):
        self.lock = threading.Lock()
        self.current_gestures = []    


    
    def main(self, mod):

        try:
        
            st.title("Prova webcam OpenCV-&-streamlit")
            
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            frame_placeholder = st.empty()

            """Main function to run the gesture recognition"""
            num_hands = 1

          

            model_path = "gesture_recognizer_semplified.task"
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
            loop_time_hand_recognized = 0
            time_text_hand_recognized = 30
            hand_chose=""

            stop_button = st.button("Ferma webcam")

            #a loop for the gesture recognition per frame
            while not stop_button:
                ret, frame = cap.read()
                if not ret:
                    st.write("Impossibile accedere alla fotocamera")
                    cap.release()
                    break

                

                #provo ad inserire qui il loop per la visione del testo che avvisa la corretta registrazione della mano
                

                # --> inserire la funzione ---> messo nel main, da togliere qui

                if loop_time_hand_recognized and time_text_hand_recognized > 0 :
                    time_text_hand_recognized -=1
                    cv2.putText(frame, "Hand chosen correctly!", (25, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
                    
                    # tecnicamente qui in base al valore della mano scelta dovrei differenziare i diversi casi
                    # in base al valore scelto passo un nome diverso a switch_page e.g. gesture_recognizer_right_complete o gesture_recognizer_right_semplified rispettivamente per la versione completa o semplificata
                    if (mod == 1) : 
                        if hand_chose == 'Left':
                            from navigation import switch_page
                            switch_page("gesture_recognizer_right_complete")
                        elif hand_chose == 'Right':
                            from navigation import switch_page
                            switch_page("gesture_recognizer_left_complete")
                    elif mod == 2:
                        if (hand_chose == 'Left'):
                            from navigation import switch_page
                            switch_page("gesture_recognizer_right_semplified")
                        elif hand_chose == 'Right':
                            from navigation import switch_page
                            switch_page("gesture_recognizer_left_semplified")

                elif time_text_hand_recognized < 0: 
                    loop_time_hand_recognized = 0


                #converting the frame to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                #processing the frame to detect hands and landmarks
                results = hands.process(frame)
                
                #flip frame
                #frame = cv2.flip(frame,1)

                #converting frame back to BGR for rendering
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                np_array = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if (flag_hand_left_or_right == 0):
                    cv2.putText(frame, "Show the hand you want to use", (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (30, 144, 255), 2, cv2.LINE_AA)
                
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

                            #!!!!!!!!!!!!!!!!--INVERTO LA CLASSIFICAZIONE IN QUANTO IL MODELLO LAVORA CON LA FOTOCAMERA FLIPPATA--!!!!!!!!!!!!!!!!!!!!!
                            if label == "Right":
                                cv2.putText(frame, "LEFT", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                                if (flag_hand_left_or_right == 0):
                                    #flag_hand_left_or_right = 1
                                    previous_hand_recognized = label


                                if count_frame_hand_recognized > 60 : 
                                    hand_chose = label
                                    flag_hand_left_or_right = 1
                                    count_frame_hand_recognized = 0
                                    loop_time_hand_recognized = 1

                                if (flag_hand_left_or_right and label != hand_chose):
                                    cv2.putText(frame, "Error! You're showing the wrong hand!", (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

                            if label == "Left":
                                cv2.putText(frame, "RIGHT", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                                if (flag_hand_left_or_right == 0):
                                # flag_hand_left_or_right = 1
                                    previous_hand_recognized = label


                                if count_frame_hand_recognized > 60 : 
                                    hand_chose = label
                                    flag_hand_left_or_right = 1
                                    count_frame_hand_recognized = 0
                                    loop_time_hand_recognized = 1



                                if (flag_hand_left_or_right and label != hand_chose):
                                    cv2.putText(frame, "Error! You're showing the wrong hand!", (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)


                            #controllo mantenimento posizione per un tempo sufficiente
                            if previous_hand_recognized == label and flag_hand_left_or_right == 0:
                                    count_frame_hand_recognized += 1
                            else: 
                                count_frame_hand_recognized = 0

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
               
                frame_placeholder.image(frame, channels="RGB")

        finally:
            if cap is not None:
                 cap.release()
            #if GestureRecognizer is not None:
                    #GestureRecognizer.close()
            cv2.destroyAllWindows()
                

                
               
        self.put_gestures(frame)
        cv2.imshow('Gesture Recognition using Mediapipe', frame)   
            
        if stop_button:
            if cap is not None:
                cap.release()
                #if GestureRecognizer is not None:
                    #GestureRecognizer.close()
            cv2.destroyAllWindows()
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
