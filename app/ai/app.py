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

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

PERSIST_DIRECTORY = f"{ROOT_DIRECTORY}/DB"

SHOW_SOURCES = False

def get_vectorstore():
    embeddings = OpenAIEmbeddings()

    vectordb = Chroma(persist_directory="/home/optizavr/htdocs/www.optizavr.com/app/ai/DB/user-" + sys.argv[2], embedding_function=embeddings)

    vectorstore = vectordb.as_retriever()

    return vectorstore

def get_conversation_chain(vectorstore):
    LLM = ChatOpenAI()

    prompt, memory = get_prompt_template(promptTemplate_type="llama", history=False)

    QA = RetrievalQA.from_chain_type(
        llm=LLM,
        chain_type="stuff",
        retriever=vectorstore,
        return_source_documents=True,
        verbose=False,
        chain_type_kwargs={
            "verbose": False,
            "prompt": prompt
        }
    )

    response = QA(QUESTION)

    res = response["result"]  # Get the answer part of the response

    # Remove any log messages from the answer
    # answer_lines = [line for line in res.split("\n") if not line.startswith(">")]

    # Join the filtered lines to reconstruct the answer
    # filtered_answer = "\n".join(answer_lines)

    # Print the filtered answer
    print(res)

    # print("Source Documents:")
    # for i, doc in enumerate(docs, start=1):
    #     print(f"Document {i}:")
    #     print(doc.page_content)
    #     print("-------------------------------------")
    
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

    user_question = QUESTION

    # create vector store
    vectorstore = get_vectorstore()

    # create conversation chain
    get_conversation_chain(vectorstore)

    # result = answer({"question": user_question})


    # print(result)

if __name__ == '__main__':
    QUESTION = sys.argv[1]

    # SOURCE_DIRECTORY = PERSIST_DIRECTORY + sys.argv[1]

    SOURCE_DIRECTORY = PERSIST_DIRECTORY + '/DB/user-' + sys.argv[2] + '/'

    main()
