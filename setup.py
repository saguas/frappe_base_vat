from setuptools import setup, find_packages
import os

version = '0.0.2'

setup(
    name='base_vat',
    version=version,
    description='Check the VAT number depending of the country.',
    author='Luis Fernandes',
    author_email='luisfmfernandes@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=["frappe","vatnumber"],
)
