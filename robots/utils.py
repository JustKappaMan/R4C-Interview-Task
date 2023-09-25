import json
from pathlib import Path
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Count
from django.http import HttpRequest

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

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


def get_last_week_report() -> tuple[datetime, dict]:
    """Return summary of robot production totals for the last week"""
    models = Robot.objects.values_list("model", flat=True).distinct()
    now = datetime.now()
    week_ago = now - timedelta(days=7)

    data = {}
    for model in models:
        # Extract each model production totals
        # e.g. ({"version": "D2", "count": "42"}, {"version": "D3", "count": "7"}, ...)
        model_data = tuple(
            Robot.objects.filter(model=model, created__range=(week_ago, now))
            .values("version")
            .annotate(count=Count("id"))
        )
        if model_data:
            data |= {model: model_data}

    return now, data


def create_xlsx_file() -> Path:
    """Save data received from `get_last_week_report()` as `.xlsx` file. Return its path."""
    wb = Workbook()
    timestamp, data = get_last_week_report()

    # Optimization. Create all of these only once since header is the same on every sheet.
    header = (("A1", "Модель"), ("B1", "Версия"), ("C1", "Количество за неделю"))
    header_font = Font(bold=True)
    header_alignment = Alignment(horizontal="center", vertical="center")

    for model, model_data in data.items():
        # Create sheet and resize table
        ws = wb.create_sheet(model)
        ws.column_dimensions["A"].width = 10
        ws.column_dimensions["B"].width = 10
        ws.column_dimensions["C"].width = 25

        # Fill table header
        for cell, value in header:
            ws[cell] = value
            ws[cell].font = header_font
            ws[cell].alignment = header_alignment

        # Fill table rows
        for row_idx, version_data in enumerate(model_data, start=2):
            ws[f"A{row_idx}"], ws[f"B{row_idx}"], ws[f"C{row_idx}"] = (
                model,
                version_data["version"],
                version_data["count"],
            )

    wb.remove(wb["Sheet"])  # Remove default empty sheet from workbook

    wb_folder = Path(settings.BASE_DIR, "reports")
    wb_folder.mkdir(parents=True, exist_ok=True)
    wb_file = wb_folder / f"report_{timestamp.strftime('%Y%m%d_%H%M%S')}.xlsx"
    wb.save(wb_file)

    return wb_file
