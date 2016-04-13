#!/bin/bash
date
echo "Deleting archive files"
rm Archive.zip
echo "Compressing AlexaSkill.js and index.js"
zip -r -X Archive.zip lambda_function.py cacert.pem config.py
