from flask_image_alchemy.fields import StdImageFile
from sqlalchemy import inspect
from werkzeug.datastructures import FileStorage


def before_delete_delete_callback(mapper, connection, instance):
    for field in mapper.attrs:
        instance_field = getattr(instance, field.key)
        if isinstance(instance_field, StdImageFile):
            instance_field.delete(variations=True)


def before_update_delete_callback(mapper, connection, instance):
    state = inspect(instance)

    for field in mapper.attrs:
        instance_field = getattr(instance, field.key)
        if isinstance(instance_field, FileStorage):
            hist = state.get_history(field.key, True)
            if hist.deleted:
                for i in hist.deleted:
                    i.delete(variations=True)
