#!/bin/bash
source env/bin/activate
export FLASK_APP=myapp
export FLASK_ENV=development
python3 app.py