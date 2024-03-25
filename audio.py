import streamlit as st
import speech_recognition as sr
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import os
from database import Database
from text import TextAnalysis
from login import Login

class AudioAnalysis:
    def __init__(self):
        self.db = Database()

    def transcribe_audio(self, audio_file, audio):
        if audio_file is not None:
            temp = "temp.wav"
            audio.export(temp, format="wav")

            recog = sr.Recognizer()
            with sr.AudioFile(temp) as src:
                audio_data = recog.record(src)

            try:
                text = recog.recognize_google(audio_data)
                sentences = [i.strip() for i in text.split(".")]
                os.remove(temp)
                return sentences

            except Exception as e:
                st.error(f"Error recognizing audio: {str(e)}")

        else:
            st.warning("Please upload an audio file.")
                    

    def visualize_audio_waveform(self, audio_data):
        if audio_data is not None:

            # Wave Graph on Amplitude VS Time
            samples = np.array(audio_data.get_array_of_samples())
            fig, ax = plt.subplots(figsize=(10, 4))
            st.subheader("Voice Graph")
            plt.plot(np.linspace(0, len(samples) / audio_data.frame_rate, num=len(samples)), samples)
            plt.title("Audio Waveform")
            plt.xlabel("Time (seconds)")
            plt.ylabel("Amplitude (m)")
            st.pyplot(fig)
        else:
            st.warning("No audio data to visualize.")

    def show_audio_analysis(self):
        if st.session_state.get('logged_in', False):
            st.title("Audio Analysis")

            if st.button("Logout", key="logout_btn2"):
                Login().logout()
                st.warning("You are not logged in. Please log in to access the homepage.")

            audio_file = st.file_uploader("Upload an audio file (supported format: '.wav' Only; duration: less than 5 minutes)", type=["wav"])

            if st.button("Submit Audio"):
            
                if audio_file is not None:
                    audio = AudioSegment.from_file(audio_file, format = audio_file.name.split(".")[-1])

                    # Save the original audio file to the temporary directory
                    text = self.transcribe_audio(audio_file, audio)[0]
                    TextAnalysis().graphical_analysis(text)

                    self.visualize_audio_waveform(audio)
            
        else:
            st.warning("You are not logged in. Please log in to access the homepage.")
