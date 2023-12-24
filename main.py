from typing import Optional, Union, Literal
from format import FormatJson


@FormatJson("example.json")
class Output:
    Stdout: str
    Stdin: str
    Type: Literal["message", "error"]
    Error: Union[str, int]
    Result: Optional[int]


output = None
try:
    output = Output()
except Exception as e:
    print(f"Error: {e}")
finally:
    if output is not None:
        print(output)
