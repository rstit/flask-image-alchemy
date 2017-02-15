from os.path import split, join

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

def create_new_filename(original_file_path, thumbnail_name):
    pathname, file_name = split(original_file_path)
    original_file_path, ext = file_name.split(".")
    new_file_name = "{old_name}.{thumbnail_name}.{ext}".format(
        old_name=original_file_path,
        thumbnail_name=thumbnail_name,
        ext=ext,
    )
    return join(pathname, new_file_name)

def process_thumbnail(file, variations, storage):
    for name, options in variations.items():
        new_file = resize_image(file, options)
        new_file_name = create_new_filename(file.name, name)
        storage.write(new_file, new_file_name)