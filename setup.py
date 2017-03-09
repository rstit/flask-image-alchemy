"""
Flask-ImageAlchemy
-------------
SQLAlchemy Standarized Image Field for Flask
"""
from setuptools import setup


setup(
    name='Flask-ImageAlchemy',
    version='0.0.7',
    url='https://github.com/rstit/flask-image-alchemy',
    license='BSD',
    author='RST-IT',
    author_email='piotr.poteralski@rst-it.com',
    description='SQLAlchemy Standarized Image Field for Flask',
    long_description=__doc__,
    packages=['flask_image_alchemy', 'flask_image_alchemy.storages'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['SQLAlchemy', 'wand', 'boto3'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)