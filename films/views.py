from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Here is the list of films for watching")

