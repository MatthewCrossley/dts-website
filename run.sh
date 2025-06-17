#!/bin/bash

cd frontend
npm run start &

cd ../backend
.venv/bin/activate
python -m fastapi run src/main.py &

wait -n
exit $?
