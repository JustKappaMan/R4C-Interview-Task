import json
from datetime import datetime as dt

from django.utils import timezone as tz
from django.http import HttpRequest

from robots.models import Robot


def _json_request_to_dict(request: HttpRequest) -> dict | None:
    """Return valid JSON from `request.body` as `dict`.
    If JSON isn't valid or doesn't use UTF-8 encoding, raise `ValueError` with corresponding message.
    """
    try:
        params = json.loads(request.body.decode("utf-8"))
    except UnicodeError:
        raise ValueError("Encoding must be 'utf-8'")
    except ValueError:
        raise ValueError("Invalid JSON")
    else:
        if not isinstance(params, dict):
            raise ValueError("Invalid JSON")

    return params


def _validate_new_robot_request(request: HttpRequest) -> dict[str, str] | None:
    """Return valid JSON that meet some requirements from `request.body` as `dict`.
    If something is wrong, raise either `TypeError` or `ValueError` with corresponding message.
    """
    params = _json_request_to_dict(request)

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
    timestamp_format = "%Y-%m-%d %H:%M:%S"
    try:
        timestamp = dt.strptime(params["created"], timestamp_format).replace(tzinfo=tz.get_default_timezone())
    except ValueError:
        raise ValueError(f"'created' must match the following pattern: '{timestamp_format}'")

    # Make sure there's no robot already assembled at that second
    if Robot.objects.is_assembled_at_second(timestamp):
        raise ValueError("A robot assembled at this second already exists")

    # Normalization. Make `model` and `version` uppercase.
    params["model"] = params["model"].upper()
    params["version"] = params["version"].upper()

    return params


def create_new_robot(request: HttpRequest) -> Robot | None:
    """Create and return new Robot using params validated with `_validate_new_robot_request`"""
    params = _validate_new_robot_request(request)

    return Robot.objects.create(
        serial=f"{params['model']}-{params['version']}",
        model=params["model"],
        version=params["version"],
        created=dt.strptime(params["created"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=tz.get_default_timezone()),
    )
