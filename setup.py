# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='django-persistent-file-widget',
    version='0.0.1',
    description='A django form file widget that persists between erroneous form submissions!',
    long_description=readme,
    author='Elijah Rutschman, Brent Sanders, Scott Meisburger',
    author_email='info+django-persistent-file-widget@sandersnewmedia.com',
    url='https://github.com/sandersnewmedia/django-persistent-file-widget',
    license=license,
    packages=find_packages(exclude=('tests',)),
    package_data={ 'persistent_widget': [ 'templates/persistent_widget/*' ] }
)
