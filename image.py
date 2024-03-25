import streamlit as st
from database import Database
from login import Login
import cv2
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

class ImageAnalysis:
    def __init__(self):
        self.db = Database()

    def detect_faces(self, uploaded_image):
        # Open the image using PIL
        image_pil = Image.open(uploaded_image)

        # Convert PIL image to NumPy array
        image_array = np.array(image_pil)

        # Convert BGR image to RGB
        img_gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        # Load pre-trained face detection model
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw bounding boxes around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img_gray, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the number of faces detected
        st.subheader("Number of Faces Detected:")
        st.write(len(faces))

    def prominent_color(self, image):
        img = Image.open(image)
        img_array = np.array(img)
        img_flat = img_array.reshape((-1, 3))

        kmeans = KMeans(n_clusters=1)
        kmeans.fit(img_flat)

        dominant_color = kmeans.cluster_centers_.astype(int)[0]
        return "#{:02x}{:02x}{:02x}".format(*tuple(dominant_color))

    def show_image_analysis(self):
        if st.session_state.get('logged_in', False):
            st.title("Image Analysis")

            if st.button("Logout", key="logout_btn4"):
                Login().logout()
                st.warning("You are not logged in. Please log in to access the homepage.")

            image_file = st.file_uploader("Upload an image file (supported format: '.jpg' or '.png' Only)", type=["jpg", "png"])

            if st.button("Submit Image"):
            
                if image_file is not None:
                    self.detect_faces(image_file)
                    st.subheader("Prominent Colour in RGB: ")
                    st.color_picker(label = "Color: ", value = self.prominent_color(image_file), disabled = True)
                    st.write("Hex Code of the Color: " + self.prominent_color(image_file))

            
        else:
            st.warning("You are not logged in. Please log in to access the homepage.")