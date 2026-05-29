from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain 
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate

from app.users.users import users
from app.memory.memory_manager import save_chat_history


import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_response(query, username):

    department = users[username]["department"]

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key= OPENAI_API_KEY
    )

    db = FAISS.load_local(
        "data/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0, api_key=OPENAI_API_KEY
    )

    prompt = PromptTemplate(
        template="""
    You are Medibot, an advanced AI medical assistant.

    Department Access:
    {department}

    Use ONLY the provided context to answer the user's question.

    Rules:
    1. Do not make up information.
    2. If the answer is not present in the context, say:
    "I could not find relevant medical information in the database."
    3. Keep answers clear and beginner friendly.
    4. Explain medical terms simply.
    5. Do not provide dangerous medical advice.
    6. Keep responses concise and accurate.

    Context:
    {context}

    Question:
    {input}

    Helpful Answer:
    """,
        input_variables=["context", "input", "department"]
    )


    document_chain = create_stuff_documents_chain( llm, prompt )

    retrieval_chain = create_retrieval_chain( retriever, document_chain )
    response = retrieval_chain.invoke({ "input": query, "department": department }) 
    answer = response["answer"]

    save_chat_history( username, query, answer ) 
    return answer



# if __name__ == "__main__":

#     username = "jay"

#     while True:

#         question = input("\nAsk Question: ")

#         if question.lower() == "exit":
#             break

#         result = get_response(
#             query=question,
#             username=username
#         )

#         print("\nMedibot Answer:\n")
#         print(result)