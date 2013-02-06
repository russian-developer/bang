#!/bin/sh
echo Creating environment
virtualenv venv

echo Install PIP inside virtual environment
./venv/bin/easy_install pip

echo Installing dependencies
# Old way
#./venv/bin/pip install -E venv -r ./build/pipreq.txt

# For pip 1.1
virtualenv venv && ./venv/bin/pip install -r ./build/pipreq.txt
