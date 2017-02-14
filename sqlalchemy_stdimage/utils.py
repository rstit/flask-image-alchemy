
def validate_variations(varations):
    #TODO check dict
    return True


def resize_image(image, options):
    #TODO process image
    return image


def process_thumbnail(file, variations, storage):
    validate_variations(variations)
    for name, options in variations.items():
        new_file = resize_image(file, options)
        new_file_name = file.name + name
        storage.write(new_file, new_file_name)