from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'chat_app/home.html', {'content':'yo'})

@csrf_exempt
def bot(request):
    #here
    return render(request, 'chat_app/index.html')



@csrf_exempt
def key(request):
    key = request.POST.get('key')
    print(key)
    return HttpResponse('key done')


@csrf_exempt
def api_message(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(1)
            user_message = data.get('messagee')
            print(2)
            key = data.get('key')
            print(3)
            if user_message:
                OPENAI_API_KEY = key
                llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
                prompt = PromptTemplate(
                input_variables=["request"],
                template='''prompt:
                    ->  give a user detail and sincere response to their question after doing critical thinking:
                    I want you to act as a wild life guide, your role is to respond to user query and response with full detail explanation about all types of animals marine and ancient or extinct wild life according to what user ask you. include all myth and facts and also example: height, weight, etc all info about user question.  follow these steps:
                    1. do critical thinking.
                    2. whenever you don't understand ask question if needed.
                    3. don't go out of scope of wild life but also write a interesting and engaging  content for user.
                    4. try to add myth and fact for all query if needed.
                    5. also talk about height and weight  and other animalogist details of that animal with references too current animals or buildings.
                    6. also write about the religion mythology that the animal follow and similarity of the animal that can also found in different religion mythology and his roles in it. 
                    7. if needed or asked by user give them powerfully story's about that wild life enhancing their experience.
                    8. also give detail information written in above prompt engaging too user.
                    9. follow up with user next question.

                    remember the prompt and act as wild life guide with a knowledge too share with other in an engaging way.

                    {request}

                    '''
                )
                chain = LLMChain(llm=llm, prompt=prompt)
                bot_response = chain.run(user_message)
                response = JsonResponse({'response':bot_response})
                response["Access-Control-Allow-Origin"] = "*" 
                return response
            else:
                return JsonResponse({"error": "Invalid message"})
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."})
    return JsonResponse({"error": "Invalid request methodsggjn."})
  