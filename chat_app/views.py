from django.shortcuts import render

def home(request):
    return render(request, 'chat_app/home.html')

# Create your views here.
# /home/harsh/git/web-chat_here/templates/chat_app/home.html
