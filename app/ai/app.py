import sys
import os
import json
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
from langchain.prompts import SystemMessagePromptTemplate
from langchain import LLMChain, PromptTemplate

"""
This file implements prompt template for llama based models. 
Modify the prompt template based on the model you select. 
This seems to have significant impact on the output of the LLM.
"""
from langchain.prompts import PromptTemplate

# this is specific to Llama-2.

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

PERSIST_DIRECTORY = f"{ROOT_DIRECTORY}/DB"

class NoOpLLMChain(LLMChain):
   """No-op LLM chain."""

   def __init__(self):
       """Initialize."""
       super().__init__(llm=ChatOpenAI(), prompt=PromptTemplate(template="", input_variables=[]))

   def run(self, question: str, *args, **kwargs) -> str:
       return question

def get_conversation_chain():
    LLM = ChatOpenAI(model_name='gpt-4-0125-preview')

    embeddings = OpenAIEmbeddings()

    vectordb = Chroma(persist_directory="/home/optizavr/htdocs/www.optizavr.com/app/ai/DB/user-" + sys.argv[2], embedding_function=embeddings)

    vectorstore = vectordb.as_retriever()

    # Load history from a file if it exists
    folder_path = 'chat_history'
    file_path = os.path.join(folder_path, sys.argv[2] + '_chat_history.json')

    if os.path.exists(file_path) and sys.argv[4] == 'false':
        os.remove(file_path)

    try:
        with open(file_path, 'r') as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []

    def save_history():
        with open(file_path, 'w') as file:

            json.dump(history, file)

    prompt = PromptTemplate(template = """Use the following pieces of context and chat history to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Context: {context}
    Chat history: {chat_history}
    Question: {question} 
    Helpful Answer:""", 
    input_variables = ["context", "question", "chat_history"])

    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

    qachat = ConversationalRetrievalChain.from_llm(
        llm=LLM, 
        get_chat_history = lambda h : h,
        verbose = True,
        # memory=memory,
        # combine_docs_chain_kwargs={'prompt': pr},
        retriever=vectorstore,  # ☜ DOCSEARCH
        return_source_documents=True        # ☜ CITATIONS
    )

    no_op_chain = NoOpLLMChain()
    # qachat.question_generator = no_op_chain

    # PROMPT 👇
    sys_prompt = """You are a helpful shop assistant, you will use the provided context (a document or documents) to answer the user"s questions.
    Read the given context before answering questions think step by step. If you can not answer a user question based on 
    the provided context, inform the user. Do not make up answers! Do not use any information other than that in the document provided to you for answering the user. Provide a detailed answer to the question. 
    Answer only in the language the user wrote in. If you you are asked about something not related to the context answer that this questions not relevant in the language the user wrote in!
    Also, take into consideration previous questions and answers.
    Context:
    {context}
    Chat History:
    {chat_history}
    Question:
    {question}
    """
    qachat.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate.from_template(sys_prompt)
    qachat.combine_docs_chain.llm_chain.prompt.input_variables = ['context', 'question', 'chat_history']

    # Create the multipurpose chain
    query = QUESTION  # ☜ Testing for memory
    result = qachat({"question": query, "chat_history": history})

    chat_hist = [(query, result["answer"])]

    history.append(chat_hist)    

    save_history()

    print(result['answer'])


def main():
    load_dotenv()

    # create conversation chain
    get_conversation_chain()

if __name__ == '__main__':
    QUESTION = sys.argv[1]

    SOURCE_DIRECTORY = PERSIST_DIRECTORY + '/DB/user-' + sys.argv[2] + '/'

    main()
