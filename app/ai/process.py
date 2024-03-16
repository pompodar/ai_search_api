import os
import sys
import json
# from haystack.document_stores import FAISSDocumentStore
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma
from chromadb.config import Settings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter



# def get_pdf_text(pdf_path):
    # with open(pdf_path, 'rb') as file:
    #     pdf_reader = PdfReader(file)
    #     text = ''
    #     for page in pdf_reader.pages:
    #         text += page.extract_text()
    # return text

def create_vectors():
    # text_splitter = CharacterTextSplitter(
    #     separator="\n",
    #     chunk_size=1000,
    #     chunk_overlap=200,
    #     length_function=len
    # )
    # chunks = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings()

    ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

    PERSIST_DIRECTORY = f"{ROOT_DIRECTORY}/user-vectors"

    # Define the Chroma settings
    CHROMA_SETTINGS = Settings(
        anonymized_telemetry=False,
        is_persistent=True,
    )

    loader = TextLoader(folder_path)
    documents = loader.load()

    # split it into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)


    vectorstore = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=PERSIST_DIRECTORY,
        client_settings=CHROMA_SETTINGS,
    )

    # vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)

    return vectorstore

def process_folder(folder_path):
    vectors = []
    for filename in os.listdir(folder_path):
        # if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        
        pdf_text = get_pdf_text(pdf_path)

        vectors.append(create_vectors(pdf_text))

    vectors = create_vectors()

    return vectors       

if __name__ == "__main__":
    load_dotenv()

    folder_path = sys.argv[1]
    vectors = process_folder(folder_path)

    # print(vectors)
