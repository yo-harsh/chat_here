import json
import os
import time
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from pdf_app.models import PdfFiles
from django.conf import settings

# View for rendering the HTML page
def render_index(request):
    return render(request, 'csv_app/index.html')  # Render the HTML template

# Temporary storage for the uploaded CSV file
# def get_file(request):
#     if request.method == 'POST':
#         obj = request.FILES['file']
#         doc = PdfFiles.objects.create(file=obj)
#         doc.save()
#         print(doc)
#     return doc


file_list = []


@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        obj = request.FILES['file']
        doc = PdfFiles.objects.create(file=obj)
        doc.save() # Access the uploaded file
        if doc:
            try:
                file_list.append(doc.file.name)
                return JsonResponse({'message': 'CSV11 uploaded successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")

# View for chatting with the bot
@csrf_exempt
def csv_agent(request):
    if request.method == 'POST':
        msg_data = json.loads(request.body.decode('utf-8'))
        msg = msg_data.get('message')
        
        if msg:
            try:
                load_dotenv()
                llm = OpenAI(temperature=0.1)
                
                
                # Assuming file_list[0] contains the relative path to the file
                relative_path = file_list[-1]


                print(relative_path)


                # Construct the absolute path using MEDIA_ROOT
                absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)


                print(absolute_path)


                # Create the CSV agent with the CSV content
                agent = create_csv_agent(llm, absolute_path,verbose=True)
                print('end')
                output = agent.run(msg)
                print('output')
                time.sleep(23)
                return JsonResponse({'output': output})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No message provided'}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")

