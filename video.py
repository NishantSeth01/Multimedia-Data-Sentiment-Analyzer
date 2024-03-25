import streamlit as st
from database import Database
from login import Login
from moviepy.video.io.VideoFileClip import VideoFileClip
from audio import AudioAnalysis
from text import TextAnalysis
from pydub import AudioSegment
import os

class VideoAnalysis:
    def __init__(self):
        self.db = Database()
    
    def convert_video_to_audio(self, uploaded_file):
        # Read the file contents
        video_contents = uploaded_file.read()

        # Set output file path (you can customize the output file name and path)
        output_file_path = "output.wav"

        with open("temp.mp4", "wb") as video_file:
            video_file.write(video_contents)

        # Load the video clip
        video_clip = VideoFileClip("temp.mp4")

        # Extract audio
        audio_clip = video_clip.audio

        # Write the audio to the output file
        audio_clip.write_audiofile(output_file_path, codec='pcm_s16le')

        # Close the video clip explicitly
        video_clip.close()
        audio_clip.close()

        return output_file_path

    def show_video_analysis(self):
        if st.session_state.get('logged_in', False):
            st.title("Video Analysis")

            # Logout Button on the navigation bar
            if st.button("Logout", key="logout_btn3"):
                Login().logout()
                st.warning("You are not logged in. Please log in to access the Page.")
            
            video_file = st.file_uploader("Upload a video file (supported format: '.mp4' Only; duration: less than 5 minutes)", type=["mp4"])
            if st.button("Submit Video"):

                if video_file is not None:
                    output_wav_file = self.convert_video_to_audio(video_file)

                    audio = AudioSegment.from_file(output_wav_file, format = "wav")
                    text = AudioAnalysis().transcribe_audio(output_wav_file, audio)[0]
                    TextAnalysis().graphical_analysis(text)
                    AudioAnalysis().visualize_audio_waveform(audio)

                    # Remove temporary file after download and audio playback
                    os.remove("temp.mp4")
                    os.remove(output_wav_file)

        else:
            st.warning("You are not logged in. Please log in to access the homepage.")