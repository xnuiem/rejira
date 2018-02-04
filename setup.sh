#!/bin/bash

sed -i -e 's/<USERNAME>/'"$PYPI_USERNAME"'/g' .pypirc
sed -i -e 's/<PASSWORD>/'"$PYPI_PASSWORD"'/g' .pypirc

cp .pypirc ~
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
rm -rf ~/.pypirc
rm -rf .pypirc