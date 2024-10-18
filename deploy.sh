flask db init
flask db migrate -m "Initial migration."
flask db upgrade
python seed.py
gunicorn run:gunicorn_app