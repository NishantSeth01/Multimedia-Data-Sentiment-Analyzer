import streamlit as st
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import yake
from database import Database
from login import Login

class TextAnalysis:
    def __init__(self):
        self.db = Database()

    
    def extract_keywords(self, text, num_keywords=5):
        custom_kw_extractor = yake.KeywordExtractor(n=1, top=num_keywords, features=None)
        keywords = custom_kw_extractor.extract_keywords(text)
        return [keyword for keyword, score in keywords]


    def analyze_text_sentiment(self, text):
        if text:
            sentiment = TextBlob(text)
            st.subheader("Text Sentiment Analysis")
            st.write(f"Polarity: {sentiment.sentiment.polarity:.2f}")
            st.write(f"Subjectivity: {sentiment.sentiment.subjectivity:.2f}")
            return sentiment
        else:
            st.warning("No text to analyze. Please upload a valid input.")

    def graphical_analysis(self, text):
        important_keywords = self.extract_keywords(text, num_keywords=5)

        # Display the most important keywords and phrases
        st.subheader("Most Important Keywords and Phrases")
        for i in range(len(important_keywords)):
            st.write((i + 1), " ", important_keywords[i])

        sentiment = self.analyze_text_sentiment(text)

        wordcloud = WordCloud().generate(text)
        st.subheader("Word Cloud")
        st.image(wordcloud.to_array())

        # Create a bar chart for sentiment polarity
        st.subheader("Sentiment Analysis: Polarity")
        fig, ax = plt.subplots()
        bars = ax.bar(["Negative", "Positive"], [sentiment.sentiment.polarity, 1-sentiment.sentiment.polarity])

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}', 
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        st.pyplot(fig)

        # Create a pie chart for sentiment subjectivity
        st.subheader("Sentiment Analysis: Subjectivity")
        fig, ax = plt.subplots()
        ax.pie([sentiment.sentiment.subjectivity, 1 - sentiment.sentiment.subjectivity], labels=["Subjective", "Objective"], autopct='%1.1f%%')
        st.pyplot(fig)

        # Create a pie chart for sentiment subjectivity
        st.subheader("Sentiment Analysis: Polarity VS Subjectivity")
        fig, ax = plt.subplots()
        ax.scatter(sentiment.sentiment.polarity, sentiment.sentiment.subjectivity)
        ax.set_xlabel("Polarity")
        ax.set_ylabel("Subjectivity")
        ax.annotate(text = (round(sentiment.sentiment.polarity, 2), round(sentiment.sentiment.subjectivity, 2)), xy = (sentiment.sentiment.polarity, sentiment.sentiment.subjectivity))
        st.pyplot(fig)

    def show_text_analysis(self):
        # Check if the user is logged in
        if st.session_state.get('logged_in', False):
            st.title("Article Analysis")

            # Logout button on the navigation bar
            if st.button("Logout", key="logout_btn1"):
                Login().logout()
                st.warning("You are not logged in. Please log in to access the Page.")

            # User input
            article_link = st.text_input("Paste the article link here:")

            if article_link:
                # Web scraping
                response = requests.get(article_link)
                soup = BeautifulSoup(response.text, 'html.parser')
                article_text = soup.get_text()

                self.graphical_analysis(article_text)
            
        else:
            st.warning("You are not logged in. Please log in to access the homepage.")
