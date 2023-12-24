from typing import Callable, Optional, Literal, Union, get_args, get_origin
import os
import json


def FormatJson(
    file: Union[str, bytes, os.PathLike]
) -> Callable[[type], Callable[[str], None]]:
    def wrapper(cls: type) -> Callable[[str], None]:
        def decorator() -> Optional[dict]:
            keys = cls.__annotations__.keys()
            types = cls.__annotations__.values()
            with open(file) as f:
                try:
                    parsed: dict = json.load(f)
                except Exception as e:
                    print(e)
                    return None
                p_keys = list(parsed.keys())
                p_values = list(parsed.values())

                for k in p_keys:
                    if k not in keys:
                        raise Exception(f"Invalid key '{k}' found in the json.")

                for k, t in zip(keys, types):
                    key = None
                    try:
                        key = p_keys.index(k)
                    except:
                        if get_origin(t) is Union and type(None) in get_args(t):
                            continue
                        raise Exception(f"Key '{k}' is not found.")

                    if key is None:
                        continue
                    val = p_values[key]
                    if get_origin(t) is Literal:
                        if val not in get_args(t):
                            raise Exception(f"Value '{val}' is not part of '{t}'")
                    elif get_origin(t) is Union:
                        if type(val) not in get_args(t):
                            raise Exception(
                                f"Type {type(val)} of value '{val}' doesn't match with '{t}'"
                            )
                    elif type(val) != t:
                        raise Exception(
                            f"Type {type(val)} of value '{val}' doesn't match with '{t}'"
                        )

            return parsed

        return decorator

    return wrapper
