import json
from http import HTTPStatus

from django.urls import reverse
from django.core import serializers
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.http import HttpRequest, HttpResponse, JsonResponse, FileResponse

from robots.utils.factory import create_new_robot
from robots.utils.xlsx import create_xlsx_file


@csrf_exempt
def new_robot_view(request: HttpRequest) -> JsonResponse:
    """JSON API endpoint for adding a new robot to DB"""
    if request.method == "POST":
        try:
            new_robot = create_new_robot(request)
        except (TypeError, ValueError) as e:
            return JsonResponse({"status": "error", "message": f"{e}"}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse(
            {
                "status": "success",
                "data": json.loads(serializers.serialize("json", [new_robot])),
            },
            status=HTTPStatus.OK,
        )
    else:
        return JsonResponse(
            {"status": "error", "message": HTTPStatus.METHOD_NOT_ALLOWED.phrase},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )


@require_GET
def last_week_stats_view(request: HttpRequest) -> HttpResponse | FileResponse:
    """Response with .xlsx file containing summary of robot production totals for the last week"""
    try:
        file_path = create_xlsx_file()
    except (Exception,):
        return redirect(reverse("last_week_stats_error_view"))
    else:
        return FileResponse(open(file_path, "rb"), status=HTTPStatus.OK)


@require_GET
def last_week_stats_error_view(request: HttpRequest) -> HttpResponse:
    """Displayed when generating a report is failed due to some exception"""
    return render(request, template_name="robots/fail.html")
