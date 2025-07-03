from core.celery import app


@app.task
def add(x, y):
    print("add: ", x + y)


@app.task
def hello():
    print("hello")
