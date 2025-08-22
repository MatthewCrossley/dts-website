# Simple To-Do List App

Simple app that tracks tasks for different users.

## Setup

You will need Python>=3.10 and a recent version of NodeJS installed.

```bash
cd frontend
npm install
cd ../backend
pip install -r requirements.txt
```

If you want to isolate the installation of the Python dependencies, you can do that in a venv. Run these commands beforehand to set that up:

```powershell
python -m venv .venv
.\venv\Scripts\activate  # or `source .venv/bin/activate` on linux/mac
```

## Running the application

You will need to run the frontend and backend in separate terminal windows.

To run the frontend:

```bash
cd frontend
npm run start
```

And the backend:
```bash
cd backend
python -m fastapi run src/main.py
```

## Testing

```bash
cd backend
pip install -r requirements-dev.txt
pytest
```
