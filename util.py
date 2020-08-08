from typing import Any, Union
from pathlib import Path
import json5


def load_json(path: Union[Path, str]) -> Any:
    with open(path) as f:
        return json5.load(f)
