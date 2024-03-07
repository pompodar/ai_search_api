import sys
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
# from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.chains import VectorDBQA
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from prompt_template_utils import get_prompt_template


# from constants import (
#     DOCUMENT_MAP,
#     EMBEDDING_MODEL_NAME,
#     INGEST_THREADS,
#     PERSIST_DIRECTORY,
# )

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

PERSIST_DIRECTORY = f"{ROOT_DIRECTORY}/DB"

SHOW_SOURCES = True

def get_vectorstore():
    embeddings = OpenAIEmbeddings()

    vectordb = Chroma(persist_directory="/home/ai_search/laravel/app/ai/DB", embedding_function=embeddings)

    vectorstore = vectordb.as_retriever()

    # print(vectorstore)

    return vectorstore


def get_conversation_chain(vectorstore):
    LLM = ChatOpenAI()
    # LLM = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":1, "max_length":512})

    # print(vectorstore.as_retriever(search_kwargs={"k": 5}))

    # qa = VectorDBQA.from_chain_type(llm=LLM, chain_type="stuff", vectorstore=vectorstore.as_retriever())

    # qa_chain = RetrievalQA.from_chain_type(
    # llm=LLM,
    # chain_type="stuff", 
    # retriever=vectorstore, 
    # return_source_documents=True)

    prompt, memory = get_prompt_template(promptTemplate_type="llama", history=False)

    QA = RetrievalQA.from_chain_type(
        llm=LLM,
        chain_type="stuff",
        retriever=vectorstore,
        return_source_documents=True,
        verbose=True,
        chain_type_kwargs={
            "verbose": True,
            "prompt": prompt
        }
    )

    response = QA("What are these documents about?")

    res, docs = response["result"], response["source_documents"]
    print(f"\nAnswer: {res}\n")

    print("Source Documents:")
    for i, doc in enumerate(docs, start=1):
        print(f"Document {i}:")
        print(doc.page_content)
        print("-------------------------------------")
    

    # print(res)

    # index = VectorStoreIndexWrapper(vectorstore=vectorstore)

    # LLM = load_model(device_type=DEVICE_TYPE, model_id=MODEL_ID, model_basename=MODEL_BASENAME)
    # prompt, memory = get_prompt_template(promptTemplate_type="llama", history=False)

    # QA = RetrievalQA.from_chain_type(
    #     llm=LLM,
    #     chain_type="stuff",
    #     retriever=RETRIEVER,
    #     return_source_documents=SHOW_SOURCES,
    #     chain_type_kwargs={
    #         "prompt": "What are these docs about?",
    #     },
    # )

    # print(vectorstore.as_retriever())
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=LLM,
        retriever=vectorstore,
        memory=memory,
    )

    return conversation_chain


def main():
    load_dotenv()

    # response = st.session_state.conversation({'question': user_question})
    # st.session_state.chat_history = response['chat_history']

    # if "conversation" not in st.session_state:
    #     st.session_state.conversation = None
    # if "chat_history" not in st.session_state:
    #     st.session_state.chat_history = None

    user_question = "What are these docs I gave you about?"

    # create vector store
    vectorstore = get_vectorstore()

    print(vectorstore)

    # create conversation chain
    get_conversation_chain(vectorstore)

    # result = answer({"question": user_question})


    # print(result)

if __name__ == '__main__':
    # SOURCE_DIRECTORY = PERSIST_DIRECTORY + sys.argv[1]

    SOURCE_DIRECTORY = PERSIST_DIRECTORY + '/DB'

    main()
