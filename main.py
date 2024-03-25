# main.py
import streamlit as st
from login import Login
from signup import Signup
from text import TextAnalysis
from audio import AudioAnalysis
from video import VideoAnalysis
from image import ImageAnalysis

def main():
    st.title("Multimedia Data Sentiment Analyzer")

    # Tabs for Login and Signup
    t1, t2, t3, t4, t5, t6 = st.tabs(["Login", "Signup", "Article Analysis", "Audio Analysis", "Video Analysis", "Image Analysis"])

    with t1:
        login = Login()
        login.login_form()

    with t2:
        signup = Signup()
        signup.signup_form()
    
    with t3:
        text = TextAnalysis()
        text.show_text_analysis()

    with t4:
        audio = AudioAnalysis()
        audio.show_audio_analysis()

    with t5:
        video = VideoAnalysis()
        video.show_video_analysis()
    with t6:
        image = ImageAnalysis()
        image.show_image_analysis()

if __name__ == "__main__":
    main()