import json
from http import HTTPStatus
from datetime import datetime

from django.core import serializers
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from robots.models import Robot


@csrf_exempt
def robots_view(request: HttpRequest) -> JsonResponse:
    match request.method:
        # case "GET":
        #     ...

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


def validate_new_robot_request(request: HttpRequest) -> dict[str, str] | None:
    """Return valid JSON from `request.body` as dict.
    If JSON doesn't meet the requirements, raise either `TypeError` or `ValueError` with corresponding message.
    """

    # Verify that JSON is valid and uses UTF-8 encoding
    try:
        params = json.loads(request.body.decode("utf-8"))
    except UnicodeError:
        raise ValueError("Encoding must be 'utf-8'")
    except ValueError:
        raise ValueError("Invalid JSON")
    else:
        if not isinstance(params, dict):
            raise ValueError("Invalid JSON")

    # Verify that JSON has all required params as strings
    required_params = ("model", "version", "created")
    if len(params) != len(required_params):
        raise ValueError(f"Request must contain exactly {len(required_params)} params")

    for param in required_params:
        if params.get(param) is None:
            raise TypeError(f"'{param}' is missing")
        if not isinstance(params[param], str):
            raise TypeError(f"'{param}' must be a string")

    # Verify that `model` and `version` are valid
    valid_length = 2
    for param in ("model", "version"):
        if len(params[param]) != valid_length or len(params[param].strip()) != valid_length:
            raise ValueError(f"'{param}' must contain exactly {valid_length} non-whitespace characters")

    # Verify that the timestamp is in the correct format
    dt_format = "%Y-%m-%d %H:%M:%S"
    try:
        dt = datetime.strptime(params["created"], dt_format)
    except ValueError:
        raise ValueError(f"'created' must match the following pattern: '{dt_format}'")

    # Make sure there's no robot already assembled at that second
    if Robot.objects.filter(created=dt).first() is not None:
        raise ValueError("A robot assembled at this second already exists")

    return params
