#!/bin/bash

sed -i -e 's/<USERNAME>/'"$PYPI_USERNAME"'/g' .pypirc
sed -i -e 's/<PASSWORD>/'"$PYPI_PASSWORD"'/g' .pypirc
