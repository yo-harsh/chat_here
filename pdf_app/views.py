from django.shortcuts import render
from django.http import HttpResponse
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
from .models import PdfFiles
import os
from django.conf import settings

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
        chunk_size=1100,
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


# Define global variables for vector database and conversation chain
global_vector_db = None
global_convo_chain = None
vector_db_lock = threading.Lock()  # Lock for thread-safety
# View for uploading a PDF file

file_list = []

@csrf_exempt
def upload_pdf(request):
    global global_vector_db, global_convo_chain
    if request.method == 'POST':
        obj = request.FILES['file']
        if obj:
            try:
                load_dotenv()
                doc = PdfFiles.objects.create(file=obj)
                doc.save()
                print('saved')
                file_list.append(doc.file.name)
                print('start')

                # Update the global variables when a new PDF is uploaded
                pdf_path = os.path.join(settings.MEDIA_ROOT, file_list[0])
                raw_text = get_pdf_text(pdf_path)
                print(0)
                chunks = get_text_chunks(raw_text)
                print(1)
                vector = get_vectordb(chunks)
                print(2)
                convo = memorydb(vector)
                print(3)

                # Lock the global variables while updating
                with vector_db_lock:
                    global_vector_db = vector
                    global_convo_chain = convo
    
            
        
                return JsonResponse({'message': 'CSV11 uploaded successfully'})
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
            try:
                load_dotenv()

                

                # Check if a PDF has been uploaded
                with vector_db_lock:
                    vector_db = global_vector_db
                    convo_chain = global_convo_chain

                if not vector_db or not convo_chain:
                    return JsonResponse({'error': 'No PDF file uploaded'}, status=400)

                # Use the stored vector database and conversation chain for chat
                output = convo_chain.run(msg)
                return JsonResponse({'output': output})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No message provided'}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")
