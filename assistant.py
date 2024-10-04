import streamlit as st
import random
import os
import openai
from PIL import Image

# logo = Image.open("cbrands_logo.jpg")
logo = Image.open("VB.png")

st.set_page_config(page_title="Assistant", initial_sidebar_state="auto" , page_icon=logo)
st.sidebar.image(logo)
st.sidebar.title("Welcome to your personal AI Sommelier")
st.sidebar.divider()
st.sidebar.subheader("How can I help you today?")

openai.api_type = st.secrets["TYPE"]
openai.api_base = st.secrets["BASE"]
openai.api_version = st.secrets["VERSION"]
openai.api_key = st.secrets["KEY"]


conversation = [

    {"role": "system", "content": "You are an AI assistant built to answer the user's questions about Constellation Brands,  "
                                "the international producer and marketer of beer and wine. "
                                "Their website is https://cbrands.com "
                                "You will help people find relevant information about the company. "
                                "Do not respond to questions about topics or domains other than Constellation Brands' area of operation. "
                                "If asked about other topics, mention that you are an assistant for Constellation Brands, and are only programmed to "
                                "answer questions about their domain or provide information about the company and its operations."
     "You can also answer questions about their subsidiary-owned products, like Kim Crawford Wines whose URL is https://www.kimcrawfordwines.com/."
     "If asked about wine suggestions or recommendations for beverages based on their wines, you can refer to https://www.kimcrawfordwines.com/, and "
     "provide suggestions based on the information on their website. For example, you could answer what are good pairings with their Prosecco, with "
     "information from this webpage https://www.kimcrawfordwines.com/collections/our-wines/products/prosecco. Or you could suggest cocktail or beverage "
     "recipes based on this webpage https://www.kimcrawfordwines.com/blogs/cocktails or this webpage https://www.kimcrawfordwines.com/blogs/recipes."
    
    }
    
    
    
    
    # {"role": "user", "content": "what are the coffee types?"},
    # {"role": "assistant", "content": "There are various types of coffee, including hot coffees, iced coffees, "
    #                                  "hot teas, iced teas, and more. Some examples of hot coffees are Caribou Coffee "
    #                                  "S'mores Cabin Latte, and Lavender Latte. Some examples of iced coffees are "
    #                                  " McCafe Iced One Step Mocha "
    #                                  "Frappe and Iced Caramel Cookie Coffee. Hot tea options include Mother Rose "
    #                                  "Best and English Breakfast Latte. Iced tea options include Iced Bubble Tea Latte."
    #                                  " Additionally, there are various desserts and more, such as Athletic Brew Co "
    #                                  "Free Wave Hazy IPA Iced Coffee and Swiss Miss S'mores Hot Cocoa."},
    # {"role": "user", "content": "what type of caramel coffees are there?"},
    # {"role": "assistant", "content": "There are several types of caramel coffees available, including Caramel Cookie "
    #                                  "Coffee, Caramel Macchiato, and Iced Caramel Cookie Coffee."}
]


if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you today?"}]

for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message(message["role"]): #, avatar=logo):
            st.write(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.write(message["content"])

prompt = st.chat_input("Say something")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    conversation.append({"role": "user", "content": prompt})

    thinking_msg = st.empty()
    thinking_msg.text("Thinking...")

    completion = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=conversation,
        temperature=0,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    chat_response = completion.choices[0].message.content

    thinking_msg.empty()
    with st.chat_message("Assistant"): #, avatar=logo):
        st.write(chat_response)

    message = {"role": "assistant", "content": chat_response}
    conversation.append(message)
    st.session_state.messages.append(message)
