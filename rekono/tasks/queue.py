from datetime import timedelta
from typing import Optional

import django_rq
from django_rq import job
from processes import executor as processes
from rq.job import Job
from tasks.exceptions import InvalidTaskException
from tasks.models import Task
from tools import executor as tools


def producer(task: Task, rekono_address: str):
    task_queue = django_rq.get_queue('tasks-queue')
    if task.scheduled_at:
        task_job = task_queue.enqueue_at(
            task.scheduled_at,
            consumer,
            task=task,
            rekono_address=rekono_address,
            on_success=scheduled_callback
        )
    elif task.scheduled_in and task.scheduled_time_unit:
        frequency = {task.scheduled_time_unit.name.lower(): task.scheduled_in}
        task_job = task_queue.enqueue_in(
            timedelta(**frequency),
            consumer,
            task=task,
            rekono_address=rekono_address,
            on_success=scheduled_callback
        )
    else:
        task_job = task_queue.enqueue(
            consumer,
            task=task,
            rekono_address=rekono_address,
            on_success=scheduled_callback
        )
    task.rq_job_id = task_job.id
    task.save()


def scheduled_callback(job, connection, result, *args, **kwargs):
    if result:
        task, rekono_address = result
        if task.repeat_in and task.repeat_time_unit:
            frequency = {task.repeat_time_unit.name.lower(): task.repeat_in}
            task_queue = django_rq.get_queue('tasks-queue')
            task_job = task_queue.enqueue_in(
                timedelta(**frequency),
                consumer.process_task,
                task=task,
                rekono_address=rekono_address,
                on_success=scheduled_callback
            )
            task.rq_job_id = task_job.id
            task.save()


@job('tasks-queue')
def consumer(task: Task = None, rekono_address: Optional[str] = None) -> tuple:
    if task:
        if task.tool:
            tools.execute(task, rekono_address)
        elif task.process:
            processes.execute(task, rekono_address)
        else:
            raise InvalidTaskException('Invalid task. Process or tool is required')
        return task, rekono_address


def cancel_and_delete_task(job_id: str) -> Job:
    tasks_queue = django_rq.get_queue('tasks-queue')
    task = tasks_queue.fetch_job(job_id)
    if task:
        task.cancel()
        task.delete()
    return task
