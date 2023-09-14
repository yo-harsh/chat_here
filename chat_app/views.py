from django.shortcuts import render
from dotenv import load_dotenv
import json
from django.http import JsonResponse
from langchain.chat_models import ChatOpenAI
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'chat_app/home.html', {'content':'yo'})

@csrf_exempt
def bot(request):
    #here
    return render(request, 'chat_app/index.html')



@csrf_exempt
def api_message(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('messagee')
            if user_message:
                load_dotenv()
                llm = ChatOpenAI()
                bot_response = llm.predict(user_message)
                response = JsonResponse({'response':bot_response})
                response["Access-Control-Allow-Origin"] = "*" 
                return response
            else:
                return JsonResponse({"error": "Invalid message"})
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."})
    return JsonResponse({"error": "Invalid request methodsggjn."})
  