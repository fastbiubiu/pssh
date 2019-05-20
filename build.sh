#!/bin/bash

pip install -r requirements.txt

pyinstaller pssh.spec

mv dist/pssh dist/pssh-$(uname -s)-$(uname -m)