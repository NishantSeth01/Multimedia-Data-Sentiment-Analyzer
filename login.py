import streamlit as st
from database import Database


class Login:
    def __init__(self):
        self.db = Database()

    def login_form(self):
        st.title("Login")
        username_login = st.text_input("Username:")
        password_login = st.text_input("Password:", type="password")

        if st.button("Login"):
            self.validate_login(username_login, password_login)

    def validate_login(self, username, password):
        user = self.db.validate_login(username, password)
        if user:
            st.success("Login successful!")
            st.session_state.logged_in = True
        else:
            st.error("Incorrect username or password")
    
    def logout(self):
        st.session_state.logged_in = False
        st.rerun()
