import os
import pickle
import time
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()


def getFaissIndex(urls):
     filePath = "faiss_vector_store.pkl"

     loader = UnstructuredURLLoader(urls=urls)
     data = loader.load()

     textSplitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
     )

     docs = textSplitter.split_documents(data)
     embeddingsObject = OpenAIEmbeddings()
     vectorStore = FAISS.from_documents(docs, embeddingsObject)

     with open(filePath, "wb") as f:
        pickle.dump(vectorStore, f)

     return filePath

def getResponseFromBot(query, filePath):
    llm = OpenAI(temperature=0.9, max_tokens=500)
    if os.path.exists(filePath):
        with open(filePath, "rb") as f:
          vectoreStore = pickle.load(f)
          chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever = vectoreStore.as_retriever)
          answer = chain({"question": query}, return_only_outputs=True)
          return answer["answer"]