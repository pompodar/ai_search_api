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
"""
This file implements prompt template for llama based models. 
Modify the prompt template based on the model you select. 
This seems to have significant impact on the output of the LLM.
"""
from langchain.prompts import PromptTemplate

# this is specific to Llama-2.

# system_prompt = """You are a helpful assistant, you will use the provided context (a document) to answer the user"s questions.
# Read the given context before answering questions and think step by step. If you can not answer a user question based on 
# the provided context, inform the user. Do not use any information other than that in the document provided to you for answering the user. Provide a detailed answer to the question. Answer only in the language the user wrote in. If you you are asked about something not related to the context answer that this questionis not relavent! in the language the user wrote in!"""

system_prompt = sys.argv[3]

def get_prompt_template(system_prompt=system_prompt, promptTemplate_type=None, history=True):
    if promptTemplate_type == "llama":
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
        SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
        if history:
            instruction = """
            Context: {history} \n {context}
            User: {question}"""

            prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            instruction = """
            Context: {context}
            User: {question}"""

            prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
    elif promptTemplate_type == "mistral":
        B_INST, E_INST = "<s>[INST] ", " [/INST]"
        if history:
            prompt_template = (
                B_INST
                + system_prompt
                + """
    
            Context: {history} \n {context}
            User: {question}"""
                + E_INST
            )
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            prompt_template = (
                B_INST
                + system_prompt
                + """
            
            Context: {context}
            User: {question}"""
                + E_INST
            )
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
    else:
        # change this based on the model you have selected.
        if history:
            prompt_template = (
                system_prompt
                + """
    
            Context: {history} \n {context}
            User: {question}
            Answer:"""
            )
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            prompt_template = (
                system_prompt
                + """
            
            Context: {context}
            User: {question}
            Answer:"""
            )
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)

    memory = ConversationBufferMemory(input_key="question", memory_key="history")

    return (
        prompt,
        memory,
    )


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

    # prompt, memory = get_prompt_template(promptTemplate_type="llama", history=True)

    custom_prompt_template = """
    ### System:
    You are an AI assistant that follows instructions extremely well. Help as much as you can.
    ### User:
    You are a research assistant for an artificial intelligence student. Use only the following information to answer user queries:
    Context= {context}
    History = {history}
    Question= {question}
    ### Assistant:
    """

    # prompt = PromptTemplate(template=custom_prompt_template,
    #                         input_variables=["question", "context", "history"])

    # memory = ConversationBufferMemory(input_key="question",
    #                                memory_key="history",
    #                                return_messages=True)

    # QA = RetrievalQA.from_chain_type(
    #     llm=LLM,
    #     chain_type="stuff",
    #     retriever=vectorstore,
    #     return_source_documents=False,
    #     verbose=False,
    #     chain_type_kwargs={
    #         "prompt": prompt,
    #         "memory": memory  
    #     }

    # )

    # chain = ConversationalRetrievalChain.from_llm(
    #     llm=LLM,
    #     retriever=vectorstore,
    # )

    # result = chain({"question": QUESTION})

    # print(result['answer'])

    prompt = PromptTemplate(template = """Use the following pieces of context and chat history to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Context: {context}
        Chat history: {chat_history}
        Question: {question} 
        Helpful Answer:""", 
        input_variables = ["context", "question", "chat_history"])

    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, input_key="question")

    # qa_chain = ConversationalRetrievalChain.from_llm(
    #     llm = LLM,
    #     retriever = vectorstore,
    #     verbose = False,
    #     memory = memory,
    #     combine_docs_chain_kwargs={"prompt": prompt},
    #     )

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

    def process_question(query, history):

        # qa_chain = ConversationalRetrievalChain.from_llm(
        #     LLM, vectorstore, memory=memory, verbose=False
        # )

        # # Call qa_chain function with the current query and chat history
        # answer = qa_chain({"question": query, "chat_history": history})['answer']
        
        # # Append the query and answer to the history
        # history.append((query, answer))

        prompt = PromptTemplate(template = """Use the following pieces of context and chat history to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Context: {context}
        Chat history: {chat_history}
        Question: {question} 
        Helpful Answer:""", 
        input_variables = ["context", "question", "chat_history"])

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
        SYSTEM_PROMPT = B_SYS + sys.argv[3] + E_SYS
        instruction = """
        Context: {context}
        Chat history: {chat_history}
        Question: {question}"""

        prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
        prompt = PromptTemplate(input_variables=["chat_history", "context", "question"], template=prompt_template)

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm = LLM,
            retriever = vectorstore,
            verbose = False,
            memory = memory,
            combine_docs_chain_kwargs={"prompt": prompt},
            )

        answer = qa_chain({"question": query, "chat_history": history})['answer']
        
        # Append the query and answer to the history
        history.append((query, answer))    

        save_history()
        
        return answer

    # Example usage
    query = QUESTION
    answer = process_question(query, history)
    print(answer) 

    # create QA chain using `langchain`, database is used as vector store retriever to find "context" (using similarity search)
    # qa = ConversationalRetrievalChain.from_llm(
    #     llm=LLM,
    #     chain_type="stuff",
    #     retriever=vectorstore,
    #     get_chat_history=lambda o:o,
    #     combine_docs_chain_kwargs={"prompt": prompt, "memory": memory},
    #     memory=memory,
    #     verbose=False,
    # )

    # # let's ask a question
    # qa({"question": QUESTION})

    # print(qa)

    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # bot = ConversationalRetrievalChain.from_llm(
    #     LLM, vectorstore, memory=memory, verbose=False
    # )

    # result = bot({"question": QUESTION})

    # print(result["answer"])

    # print(result["answer"])

    # response = QA({"query": QUESTION})

    # res = response["result"]  # Get the answer part of the response

    # Remove any log messages from the answer
    # answer_lines = [line for line in res.split("\n") if not line.startswith(">")]

    # Join the filtered lines to reconstruct the answer
    # filtered_answer = "\n".join(answer_lines)

    # Print the filtered answer
    # res = res.replace('<<SYS>>', '').replace('[INST]<<SYS>> ', '').replace('<</SYS>>', '').replace('[INST]<<SYS>>', '')
    # print(prompt)

    # print("Source Documents:")
    # for i, doc in enumerate(docs, start=1):
    #     print(f"Document {i}:")
    #     print(doc.page_content)
    #     print("-------------------------------------")
    
    # memory = ConversationBufferMemory(
    #     memory_key='chat_history', return_messages=True)
    
    # conversation_chain = ConversationalRetrievalChain.from_llm(
    #     llm=LLM,
    #     retriever=vectorstore,
    #     memory=memory,
    # )

    # return conversation_chain


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
    answer = get_conversation_chain(vectorstore)

    # result = answer({"question": user_question})

    # print(result)

if __name__ == '__main__':
    QUESTION = sys.argv[1]

    # SOURCE_DIRECTORY = PERSIST_DIRECTORY + sys.argv[1]

    SOURCE_DIRECTORY = PERSIST_DIRECTORY + '/DB/user-' + sys.argv[2] + '/'

    main()
