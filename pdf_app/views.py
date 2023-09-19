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
from .models import PdfFiles
import os
from django.conf import settings
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

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
def get_vectordb(chunks,key):
    embeddings = OpenAIEmbeddings(openai_api_key=key)
    vectordb = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectordb

# Function to set up conversation memory
def memorydb(vectordb,key):
    llm = ChatOpenAI(openai_api_key=key)
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
    print(1)
    key1 = request.POST.get('key')
    print(key1)
    global global_vector_db, global_convo_chain
    if request.method == 'POST':
        
        obj = request.FILES['file']
        if obj:
            try:
                # load_dotenv()
                print(key1)
                OPENAI_API_KEY = key1
                print(OPENAI_API_KEY)
                doc = PdfFiles.objects.create(file=obj)
                doc.save()
                print('saved')
                file_list.append(doc.file.name)
                print(file_list[0])
                print('start')

                # Update the global variables when a new PDF is uploaded
                pdf_path = os.path.join(settings.MEDIA_ROOT, file_list[0])
                raw_text = get_pdf_text(pdf_path)
                print(0)
                chunks = get_text_chunks(raw_text)
                print(1)
                vector = get_vectordb(chunks,OPENAI_API_KEY)
                print(2)
                convo = memorydb(vector,OPENAI_API_KEY)
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
                # load_dotenv()

                

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



# 
# 
# 

# content_list = []


# @csrf_exempt
# def pdf_download(request):
#     if request.method == 'POST':
#         pdf_data = json.loads(request.body.decode('utf-8'))
#         pdf_text = pdf_data.get('pdf_text')
        
#         if pdf_text:
# 	        # Create Bytestream buffer
#             buf = io.BytesIO()
#             # Create a canvas
#             c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
#             # Create a text object
#             textob = c.beginText()
#             textob.setTextOrigin(inch, inch)
#             textob.setFont("Helvetica", 14)

#             # Add some lines of text
#             # lines = [
#             #     "This is line 1",
#             #     "This is line 2",
#             #     "This is line 3",
#             # ]
            

            
            
#             # Designate The Model
#             # venues = Venue.objects.all()

#             # # Create blank list
#             # lines = []

#             # for venue in venues:
#             # 	lines.append(venue.name)
#             # 	lines.append(venue.address)
#             # 	lines.append(venue.zip_code)
#             # 	lines.append(venue.phone)
#             # 	lines.append(venue.web)
#             # 	lines.append(venue.email_address)
#             # 	lines.append(" ")

#             # Loop
#             # for line in lines:
#             #     textob.textLine(line)

#             print('start')
#             textob.textLine(pdf_text)
#             # Finish Up
#             c.drawText(textob)
#             c.showPage()
#             c.save()
#             buf.seek(0)
#             print('done')
#             # Return something
#             return FileResponse(buf, as_attachment=True, filename='content.pdf')
            
#         else:
#             JsonResponse({'error': 'No message provided'}, status=400)
#     else:
#         return HttpResponseBadRequest("Invalid request method")
    
# @csrf_exempt
# def pdf_download(request):
#     if request.method == 'GET':
#         print('deliverd')
#         return FileResponse(content_list[0], as_attachment=True, filename='content.pdf')
#     else:
#         return HttpResponseBadRequest("Invalid request method")


# Global variable to store pdf_text
pdf_text = None

@csrf_exempt
def pdf_download(request):
    global pdf_text
    
    if request.method == 'POST':
        pdf_data = json.loads(request.body.decode('utf-8'))
        pdf_text = pdf_data.get('pdf_text')


        print('got it')
        return JsonResponse({'done': 'got message for download'})
        
    elif request.method == 'GET':
        if pdf_text:

            pdf_lines = pdf_text.split('\n')
            # ■
            print(pdf_text)
            print('*'*5)
            # print(pdf_lines)
            # Create Bytestream buffer
            buf = io.BytesIO()
            # Create a canvas
            c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
            # Create a text object
            textob = c.beginText()
            textob.setTextOrigin(inch, inch)
            textob.setFont("Helvetica", 14)
            
            for line in pdf_lines:
                # Manually split long lines into smaller chunks
                chunk_size = 60 # Adjust this value as needed
                for i in range(0, len(line), chunk_size):
                    chunk = line[i:i + chunk_size]
                    textob.textLines(chunk)

            # textob.textLine(pdf_text)
            
            # Finish Up
            c.drawText(textob)
            c.showPage()
            c.save()
            buf.seek(0)
            
            # Return the PDF response for GET requests
            response = FileResponse(buf, as_attachment=True, filename='content.pdf')
            
            # Reset pdf_text after generating the PDF
            pdf_text = None
            
            return response
        else:
            return JsonResponse({'error': 'No message not available for download'}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")
# Now, the pdf_text variable is reset to None after generating and serving the PDF for both POST and GET requests, ensuring that each PDF generated from the pdf_download view contains only the most recent text provided in the POST request.





