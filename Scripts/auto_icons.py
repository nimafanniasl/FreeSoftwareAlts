import re
import requests
import json
import os

# --------------------------------------------------- #

ICON_WIDTH = "30px"

SCREENSHOTS_WIDTH = "25%"
SCREENSHOTS_HEIGHT = "auto"

# --------------------------------------------------- #

api_content = json.loads(
    requests.get(f"https://f-droid.org/repo/index-v2.json").content
    )["packages"]

# api_content = json.loads(open("ignore_dir/index-v2.json", "r").read())["packages"]

# Define a function to get the package name from the F-Droid URL
def get_package_name(url: str):
    return url.split("/")[-2].replace("/", "")


def generate_img_tag(img_url):
    img_tag = f'<img data-src="{img_url}" class="lazy app-icon" width="{ICON_WIDTH}">'
    return img_tag

def get_icon(package_name):
    package = api_content[package_name]["metadata"]
    try:
        icon = package["icon"]
    except KeyError:
        return None

    try:
        try:
            icon_link = "https://f-droid.org/repo" + icon["fa-IR"]["name"]
        except KeyError:
            icon_link = "https://f-droid.org/repo" + icon["en-US"]["name"]
    except:
        return None

    return generate_img_tag(icon_link)

def process_file(file_path):
    # Open the file for reading
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Regular expression pattern to match F-Droid links
    fdroid_pattern = re.compile(r"https?://(?:www\.)?f-droid\.org/.*/(.*?)\)")
    img_pattern = re.compile(r"<img data-src=\".*\" class=\".*app-icon\".*>")

    # Create a new list to store modified lines
    new_lines = []

    # Iterate through the lines
    for line in lines:
        if img_pattern.search(line) or "<!-- NoIcon -->" in line:
            new_lines.append(line)  # Add unchanged line to new list
            continue

        match = fdroid_pattern.search(line)
        if match:
            package_name = match.group(1)
            img_tag = get_icon(package_name)
            if img_tag is None:
                img_tag = "<!-- NoIcon -->"
            new_lines.append(f"{img_tag}{line}")  # Add modified line to new list
        else:
            new_lines.append(line)  # Add unchanged line to new list

    # Write the modified content back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(new_lines)

if __name__ == "__main__":
    folder = "docs/android"
    files = os.listdir(folder)
    for file in files:
        process_file(f"{folder}/{file}")
