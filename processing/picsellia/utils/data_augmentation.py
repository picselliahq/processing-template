from PIL import Image
from pathlib import Path
import os

def simple_rotation(filepaths: list, target_path: str):
    Path(target_path).mkdir(parents=True, exist_ok=True)
    for path in filepaths:
        filename = Path(path).name
        image = Image.open(path)
        rotated_image = image.rotate(45)
        rotated_image.save(os.path.join(target_path, filename))