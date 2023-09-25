import json
from http import HTTPStatus
from datetime import datetime

from django.core import serializers
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from robots.models import Robot
from robots.utils import validate_new_robot_request, get_last_week_report


@csrf_exempt
def robots_view(request: HttpRequest) -> JsonResponse:
    match request.method:
        case "GET":
            return JsonResponse(
                {
                    "status": "success",
                    "data": get_last_week_report(),
                },
                status=HTTPStatus.OK,
            )

        case "POST":
            try:
                params = validate_new_robot_request(request)
            except (TypeError, ValueError) as e:
                return JsonResponse({"status": "error", "message": f"{e}"}, status=HTTPStatus.BAD_REQUEST)

            new_record = Robot.objects.create(
                serial=f"{params['model']}-{params['version']}",
                model=params["model"],
                version=params["version"],
                created=datetime.strptime(params["created"], "%Y-%m-%d %H:%M:%S"),
            )

            return JsonResponse(
                {
                    "status": "success",
                    "data": json.loads(serializers.serialize("json", [new_record])),
                },
                status=HTTPStatus.OK,
            )

        case _:
            return JsonResponse(
                {
                    "status": "error",
                    "message": HTTPStatus.METHOD_NOT_ALLOWED.phrase
                },
                status=HTTPStatus.METHOD_NOT_ALLOWED,
            )
