from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "JJE_Waivers/waivers_index.html")
