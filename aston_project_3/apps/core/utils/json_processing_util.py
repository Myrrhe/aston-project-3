"""Some methods to process json files."""
import json

from django.apps import apps
from django.db.models import Model


def count_instance(path: str) -> int:
    """Count the number of objects in a json file."""
    with open(path, "r") as f:
        obj_json = json.load(f)
        res = len(obj_json)
    f.close()
    return res


def get_model_from_str(model_str: str) -> type[Model]:
    """Get a model from a string containing the app name and the model name."""
    str_splitted = model_str.split(".")
    return apps.get_model(
        app_label=str_splitted[0],
        model_name=str_splitted[1]
    )


def fk_exists(field: any, value_fk: any, obj_json: any) -> bool:
    """
    Check if a foreign key (field and value_fk) can be found.

    Look in the database and the JSON file as well.
    """
    fk_found = False
    if field.related_model.objects.filter(pk=value_fk):
        fk_found = True
    else:
        for fk_obj in obj_json:
            if (
                get_model_from_str(fk_obj["model"]) == field.related_model
                and fk_obj["pk"] == value_fk
            ):
                fk_found = True
    return fk_found
