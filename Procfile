web: uvicorn src.main:app --host=0.0.0.0 --port=${PORT:-5000}

web: gunicorn my-application.wsgi --log-file -