from xml.etree import ElementTree


def find_min_images_count(filename):
    tree = ElementTree.parse(filename)
    root = tree.getroot()

    images = [
        len(list(page.iterfind('.//fragment[@type="image"]'))) for page in root
    ]

    return min(images)
