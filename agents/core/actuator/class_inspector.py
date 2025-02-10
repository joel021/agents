import inspect
from typing import Dict, Any
from mongoengine import Document, StringField, ListField, ReferenceField, EnumField

from agents.core.dto.llm_schema import ArgumentSchema
from agents.core.dto.response import Response


def get_class_description(cls, cls_instance) -> Dict[str, Dict[str, Any]]:
    class_description = {}
    for name, method in inspect.getmembers(cls):
        if inspect.isfunction(method):
            signature = inspect.signature(method)
            arg_descriptions = {}

            # Skip the 'self' parameter:
            parameters = list(signature.parameters.values())[1:]  # Slice to remove the first parameter ('self')

            for param in parameters:  # Iterate over the remaining parameters
                arg_name = param.name
                arg_type = param.annotation

                if arg_type is inspect._empty:
                    arg_type_str = "(any)"
                elif hasattr(arg_type, '__name__'):
                    arg_type_str = f"({arg_type.__name__})"
                elif hasattr(arg_type, '__origin__'):
                    arg_type_str = f"({arg_type._name})"
                    if hasattr(arg_type, '__args__'):
                        arg_type_str += "["
                        for i, a in enumerate(arg_type.__args__):
                            if hasattr(a, '__name__'):
                                arg_type_str += a.__name__
                            else:
                                arg_type_str += str(a)
                            if i < len(arg_type.__args__) - 1:
                                arg_type_str += ", "
                        arg_type_str += "]"
                else:
                    arg_type_str = f"({str(arg_type)})"

                required = "(required)" if param.default is inspect._empty else "(optional)"
                arg_descriptions[arg_name] = f"{arg_type_str} {required}"

            bound_method = getattr(cls_instance, name)
            class_description[name] = {
                "function": bound_method,
                "args": arg_descriptions
            }
    return class_description


def db_class_model_describer(cls, visited=None):
    if visited is None:
        visited = set()

    if cls in visited:
        return "Recursive Reference"

    visited.add(cls)
    result = {}

    for attr, value in cls.__dict__.items():

        if "_" == attr[0:1]:
            continue

        if isinstance(value, EnumField):
            result[attr] = ", ".join(e.name for e in value.choices)
        elif isinstance(value, StringField):
            result[attr] = "StringField"
        elif isinstance(value, ListField):
            if isinstance(value.field, ReferenceField):
                result[attr] = [db_class_model_describer(value.field.document_type, visited)]  # List of nested descriptions
            elif isinstance(value.field, StringField):
                result[attr] = ["StringField"]
            elif isinstance(value.field, EnumField):
                result[attr] = [", ".join(e.name for e in value.field._enum)]
            else:
                result[attr] = [value.field.__class__.__name__]
        elif isinstance(value, ReferenceField):
            result[attr] = db_class_model_describer(value.document_type, visited)  # Recursive call
        elif isinstance(value, type) and issubclass(value, Document):
            result[attr] = db_class_model_describer(value, visited)  # Recursive call for nested classes

    visited.remove(cls)

    return result

def execute_function(action_dict: dict, available_functions: dict) -> Response:

    function_name = action_dict.get("function_name", None)
    if not function_name:
        return Response(f"function_name not provided in the request. Probably the schema is wrong.", True)

    function_callable = available_functions.get(function_name, {}).get("function", None)
    if not function_callable:
        return Response(f"Unsupported instruction: {function_name}", True)

    args_dict = convert_to_dict(action_dict.get("arguments", []))
    try:
        return function_callable(**args_dict)
    except Exception as e:
        return Response(f"Error executing instructions: {e}", True)

def convert_to_dict(argument_responses: list[ArgumentSchema]) -> dict:
    args = {item['arg']: item['value'] for item in argument_responses}
    return {k: v for k, v in args.items() if v is not None}
