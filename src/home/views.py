from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def index_view(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="home/index.html")
