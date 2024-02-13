import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)


def scrape_website(url):
    """Scrape website content from the given URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extracting text from the webpage; this might need adjustments
        # depending on the website's structure
        text = ' '.join(p.get_text() for p in soup.find_all('p'))
        return text
    except Exception as e:
        return f"An error occurred: {e}"
    

def summarize_text(text, max_length=30):
    """Summarize the given text to a specified maximum word length using OpenAI."""
    response = openai.chat.completions.create(
    model="gpt-4-1106-preview",  # or another suitable model
        messages=[
        {   "role": "system",
        "content" : "You are the best digital marketing agency. You are helping your client 2D3D to promote independent creative artists with the latest event. ",
            "role":"user",
        "content": f"Summarize this text in {max_length} words: {text} in a creative way to encourage users to find out more. The text need to be suitable for social media platforms like facebook, instagram.",
        
        }
    ]
    )
    return response.choices[0].message.content

# Streamlit app
def main():
    st.title('Social Media')
    content = ""    
    # User choice for input type
    name = st.text_input("Enter your company name")
    website_url = st.text_input("Enter the website URL to summarize:")
    if website_url:
        with st.spinner('Scraping website content...'):
            content = scrape_website(website_url)
            if not content:
                st.error("Failed to scrape the website or the website is empty.")

    content = content + " " + st.text_area("Enter the text to summarize:")
    print(content)

    if st.button('Summarize'):
        if content and content.strip():
            with st.spinner('Summarizing content...'):
                summary = summarize_text(content, 30) + f" {name} will be exhibiting at the Royal Highland Show"
            st.success("Summary generated successfully!")
            st.write(summary)
        else:
            st.error("Please enter a valid URL or text to summarize.")

if __name__ == "__main__":
    main()