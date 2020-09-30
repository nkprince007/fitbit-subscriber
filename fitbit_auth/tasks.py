from subscriber import celery


@celery.task
def add(first, second):
    return first + second
