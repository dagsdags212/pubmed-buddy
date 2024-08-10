from pathlib import Path
import tomllib
from typing import Dict, Any

DATA_DIR = Path(__file__).parent


def load_toml_files() -> Dict[str, Any]:
    global DATA_DIR
    config = {}
    for toml_file in DATA_DIR.glob("*.toml"):
        with open(toml_file, "rb") as toml:
            cfg = tomllib.load(toml, parse_float=float)
            config[toml_file.stem] = cfg
    return config


CONFIG = load_toml_files()
