from src.core.types.models import Model


def create_dict_from_model(
    model: Model,
    exclude_fields: list[str] = [  # noqa
        "created_at",
        "updated_at",
        "id",
    ],
    all_examples: bool = False,
) -> dict:
    result = {}
    json_schema = model.model_json_schema()
    for column, property in json_schema["properties"].items():
        if column not in exclude_fields:
            if list_of_examples := property.get("examples"):
                result[column] = list_of_examples if all_examples else list_of_examples[0]
            else:
                result[column] = property.get("default")
    return result
