import json
from datetime import datetime, timedelta

from django.db.models import Count
from django.http import HttpRequest

from robots.models import Robot


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


def get_last_week_report() -> dict:
    models = tuple(Robot.objects.values_list("model", flat=True).distinct())
    last_week_end = datetime.now()
    last_week_start = last_week_end - timedelta(days=7)

    result = {}
    for model in models:
        model_data = tuple(
            Robot.objects.filter(model=model, created__range=(last_week_start, last_week_end))
            .values("version")
            .annotate(count=Count("id"))
        )
        result |= {model: model_data}

    return result
