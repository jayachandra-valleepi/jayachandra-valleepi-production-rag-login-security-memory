import os

from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

pdf_folder = "./data"


documents = []

for file in os.listdir(pdf_folder):

    if file.endswith(".pdf"):

        path = os.path.join(pdf_folder, file)

        print(f"Loading : {file}")

        loader = PyPDFLoader(path)

        documents.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(
chunk_size=1000,
chunk_overlap=200
)
docs = splitter.split_documents(documents)


embeddings = OpenAIEmbeddings(
model="text-embedding-3-small", api_key=OPENAI_API_KEY
)

db = FAISS.from_documents(
docs,
embeddings
)


db.save_local("data/faiss_index")

print("FAISS Index Created Successfully")