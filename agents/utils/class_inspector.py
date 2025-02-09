import inspect
from typing import Dict, Any

def get_class_description(cls, cls_instance) -> Dict[str, Dict[str, Any]]:
    class_description = {}
    for name, method in inspect.getmembers(cls):
        if inspect.isfunction(method):
            signature = inspect.signature(method)
            arg_descriptions = {}

            for param in signature.parameters.values():
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

            bound_method = getattr(cls_instance, name) # Get the bound method
            class_description[name] = {
                "function": bound_method,  # Store the bound method
                "args": arg_descriptions
            }
    return class_description
