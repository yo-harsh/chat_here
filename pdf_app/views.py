from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponseBadRequest
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from django.views.decorators.csrf import csrf_exempt
import threading  # Import threading to ensure thread-safety
from dotenv import load_dotenv

# Global variable to store the vector database temporarily
global_vector_db = None
vector_db_lock = threading.Lock()  # Lock for thread-safety

# Function to get text from a PDF file
def get_pdf_text(pdf_docs):
    text = ""
    pdf_reader = PdfReader(pdf_docs)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create a vector database
def get_vectordb(chunks):
    embeddings = OpenAIEmbeddings()
    vectordb = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectordb

# Function to set up conversation memory
def memorydb(vectordb):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    convo_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectordb.as_retriever(), memory=memory)
    return convo_chain

# View for rendering the HTML page
def render_index(request):
    return render(request, 'pdf_app/index.html')  # Render the HTML template

# View for uploading a PDF file
@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST':
        file_data = request.FILES.get('file')  # Access the uploaded file
        if file_data:
            try:
                global global_vector_db  # Access the global vector database variable
                with vector_db_lock:
                    load_dotenv()
                    raw_text = get_pdf_text(file_data)
                    chunks = get_text_chunks(raw_text)
                    global_vector_db = get_vectordb(chunks)  # Store the vector database
                return JsonResponse({'message': 'PDF uploaded successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")

# View for chatting with the bot
@csrf_exempt
def chat_with_bot(request):
    if request.method == 'POST':
        msg_data = json.loads(request.body.decode('utf-8'))
        msg = msg_data.get('message')
        
        if msg:
            load_dotenv()
            try:
                with vector_db_lock:
                    convo = memorydb(global_vector_db)  # Use the stored vector database
                output = convo.run(msg)
                return JsonResponse({'output': output})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No message provided'}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")
