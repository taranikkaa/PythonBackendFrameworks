from django.shortcuts import HttpResponse
def hello_view(request):
    return HttpResponse("Course Management API is running")

