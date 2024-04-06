import re
import requests
from bs4 import BeautifulSoup

TAG_START = "<!-- F-droid app screenshots -start -->\n"
TAG_END = "\n<!-- F-droid app screenshots -end -->"

TAG_NO_IMAGE = "\n<!-- F-droid app screenshots -NoImageExists -->\n"

# --------------------------------------------------- #

IMG_WIDTH = "25%"
IMG_HEIGHT = "auto"

# --------------------------------------------------- #


# Define a function to get the package name from the F-Droid URL
def get_package_name(url: str):
    return url.split("/")[-2].replace("/", "")


def generate_img_tag(img_url):
    img_tag = f'<img src="{img_url}" width="{IMG_WIDTH}" height="{IMG_HEIGHT}">'
    return img_tag


def get_pics(package_name):
    image_links = []
    image_tags = []

    html = requests.get(f"https://f-droid.org/fa/packages/{package_name}/").content
    soup = BeautifulSoup(html, "html.parser")
    lis = soup.find_all("li", attrs={"class": ["js_slide", "screenshot"]})

    for li in lis:
        img = li.find("img")
        image_links.append(img.get("src"))
        if len(image_links) == 4:
            break

    for image_link in image_links:
        image_tags.append(generate_img_tag(image_link))

    image_tags_str = "".join(image_tags)

    if image_tags_str != "":
        image_tags_str = f"{TAG_START}{image_tags_str}{TAG_END}"
    else:
        image_tags_str = TAG_NO_IMAGE

    return image_tags_str


# Define the main function to process the file
def process_file(file_path):
    # Open the file for reading
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Regular expression pattern to match F-Droid links
    fdroid_pattern = re.compile(r"\((https?://(?:www\.)?f-droid\.org[^)]+)\)")

    # Iterate through the lines
    for i, line in enumerate(lines):
        match = fdroid_pattern.search(line)
        if match:
            package_name = get_package_name(match.group(1))
            # Check if additional text exists after the line
            if (
                i < len(lines) - 1
                and not lines[i + 1].startswith(TAG_START)
                and not lines[i + 1].startswith(TAG_NO_IMAGE)
            ):
                # Call get_pics function to retrieve additional text
                additional_text = get_pics(package_name)
                # Insert additional text after the line
                lines.insert(i + 1, additional_text + "\n")

    # Write the modified content back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)


if __name__ == "__main__":
    process_file("docs/اندروید.md")
