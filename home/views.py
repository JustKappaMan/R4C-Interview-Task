from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed


def index_view(request: HttpRequest) -> HttpResponse | HttpResponseNotAllowed:
    if request.method == "GET":
        return render(request, template_name="home/index.html")
    else:
        return HttpResponseNotAllowed(permitted_methods=("GET",))
