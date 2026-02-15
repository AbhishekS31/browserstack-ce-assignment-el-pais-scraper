import os
import requests

def download_image(image_url, index):
    if not image_url:
        return

    os.makedirs("output", exist_ok=True)

    filename = f"article_{index}.jpg"
    filepath = os.path.join("output", filename)

    response = requests.get(image_url)

    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)
