from wand.image import Image as WandImage


def validate_variations(variations):
    for key, value in variations.items():
        if not isinstance(key, str):
            raise ValueError("Variation name should be `str` type")
        if not isinstance(value, dict):
            raise ValueError("Variation should contains `dict`")
        if 'height' not in value.keys():
            raise ValueError("Missing 'height' value")
        if 'width' not in value.keys():
            raise ValueError("Missing 'width' value")
    return variations


def resize_image(image_file, options):
    img = WandImage(file=image_file)
    img.resize(
        height=options.get('height'),
        width=options.get('width')
    )
    return img


def process_thumbnail(file, variations, storage):
    for name, options in variations.items():
        new_file = resize_image(file, options)
        new_file_name = file.name + name
        new_file_name = "test.png"
        storage.write(new_file, new_file_name)