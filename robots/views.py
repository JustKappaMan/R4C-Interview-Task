import json
from http import HTTPStatus
from datetime import datetime as dt

from django.urls import reverse
from django.core import serializers
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.utils.timezone import get_default_timezone
from django.http import HttpRequest, HttpResponse, JsonResponse, FileResponse

from robots.models import Robot
from robots.utils import validate_new_robot_request, create_xlsx_file


@csrf_exempt
def new_robot_view(request: HttpRequest) -> JsonResponse:
    """JSON API endpoint for adding a new robot to DB"""
    if request.method == "POST":
        try:
            params = validate_new_robot_request(request)
        except (TypeError, ValueError) as e:
            return JsonResponse({"status": "error", "message": f"{e}"}, status=HTTPStatus.BAD_REQUEST)

        new_robot = Robot.objects.create(
            serial=f"{params['model']}-{params['version']}",
            model=params["model"],
            version=params["version"],
            created=dt.strptime(params["created"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=get_default_timezone()),
        )

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
def last_week_stats_view(request: HttpRequest) -> FileResponse:
    """Response with .xlsx file containing summary of robot production totals for the last week"""
    try:
        file_path = create_xlsx_file()
    except (Exception,) as e:
        print(e)
        return redirect(reverse("last_week_stats_error_view"))
    else:
        return FileResponse(open(file_path, "rb"), status=HTTPStatus.OK)


@require_GET
def last_week_stats_error_view(request: HttpRequest) -> HttpResponse:
    """Displayed when generating a report is failed due to some exception"""
    return render(request, template_name="robots/fail.html")
