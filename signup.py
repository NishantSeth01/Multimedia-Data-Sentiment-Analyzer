import streamlit as st
from database import Database
from mysql.connector import IntegrityError

class Signup:
    def __init__(self):
        self.db = Database()

    def signup_form(self):
        st.title("Signup")
        new_username_signup = st.text_input("Choose a username:")
        new_password_signup = st.text_input("Choose a password:", type="password")

        if st.button("Signup"):
            self.validate_signup(new_username_signup, new_password_signup)

    def validate_signup(self, username, password):
        try:
            existing_user = self.db.validate_signup(username)
            if len(username) == 0 or len(password) == 0:
                st.error("Username or password cannot be empty")
            elif len(password) < 8 and password.isalnum() == True:
                st.error("Password should have less than 8 character or doesn't consist of alphabet & number")
            else:
                self.db.insert_user(username, password)
                st.success("Signup successful! You can now login.")
        except IntegrityError:
            st.error("Username already exists. Please choose a different one.")
