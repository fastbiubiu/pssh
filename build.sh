#!/bin/bash

pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

pyinstaller pssh.spec

mv dist/pssh dist/$(uname -s)-$(uname -m)-pssh