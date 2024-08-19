import streamlit as st
from langchainHelper import getFaissIndex,getResponseFromBot

st.title("Url Research Bot")
st.sidebar.title("Provide Url for fecthing information:")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

processUrlClicked = st.sidebar.button("Process Url")

main_placeholder = st.empty()

if processUrlClicked:
     main_placeholder.text("Data Loading...Started...✅✅✅")
     filePath = getFaissIndex(urls=urls)
     main_placeholder.text("Vector Embeddings...Completed...✅✅✅")

query  = main_placeholder.text_input("Question: ")
if query:
     answer = getResponseFromBot(query=query, filePath=filePath)
     st.header("Here is your Answer")
     st.write(answer)
