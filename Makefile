run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

add:
	pip install $(package)
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

format:
	black .

test:
	pytest

docker-build:
	docker build -t my-fastapi-app .

docker-run:
	docker run -p 8000:8000 my-fastapi-app

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
