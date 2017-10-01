#!/usr/bin/env python

from setuptools import setup

setup(name='listats',
      version='1.0',
      description='LiveInternet stat reader',
      author='Andrey Khokhlin',
      author_email='khokhlin@gmail.com',
      url='https://github.com/khokhlin/listats/',
      packages=['listats'],
      install_requires=["pillow"],
      entry_points={
          "console_scripts": [
              "listats = listats.listats:main",
          ]
      }
 )
