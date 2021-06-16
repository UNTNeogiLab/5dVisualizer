import os
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

visualizers = {}
extensions = {}
for directory in os.scandir(str(Path(__file__).resolve().parent)):
    if directory.is_dir():
        for file in os.listdir(directory):
            if str(file).__contains__("D.py"):
                sname = file.replace(".py", "")
                try:
                    module = import_module(f"{__name__}.{directory.name}.{sname}")
                except ImportError:
                    print(f"{file} import failed")
                else:
                    visualizers[module.name] = module
                    types[module.name] = module.type
