#!/bin/bash

# pytest and coverage
pytest --disable-pytest-warnings --cov=chepy tests/

# bandit
bandit --recursive chepy/ --ignore-nosec --skip B101,B413,B303,B310,B112,B304

# docs
cd docs
make clean html
cd ..
