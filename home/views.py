from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed


@require_GET
def index_view(request: HttpRequest) -> HttpResponse | HttpResponseNotAllowed:
    return render(request, template_name="home/index.html")
