#! /bin/bash

rm -r build
pip install poetry

poetry install --no-dev
mkdir build && cd build
cp -r $(poetry env info -p)/lib/*/site-packages/* .
cp -r ../ai_engine .
zip -r ../cr-ai-ai-engine-dev.zip .