import json
from datetime import datetime
from pathlib import Path
from typing import Any


def save_json(
    save_directory: str,
    save_name: str,
    data: Any,
    timestamp: datetime | None = None,
) -> None:
    if timestamp:
        timestamp = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        save_path = Path(save_directory) / f"{save_name}_{timestamp}.json"

    else:
        save_path = Path(save_directory) / f"{save_name}.json"

    with open(save_path, "w") as f:
        json.dump(data, f, indent=4)
