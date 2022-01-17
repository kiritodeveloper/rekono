import os
import signal

from django.core.exceptions import ValidationError
from django.utils import timezone
from executions.models import Execution
from executions.queue.utils import cancel_job
from tasks.enums import Status
from tasks.queue import cancel_and_delete_task


def cancel_task(task):
    if (
        task.status != Status.CANCELLED and
        (
            task.status in [Status.REQUESTED, Status.RUNNING] or
            (task.repeat_in and task.repeat_time_unit)
        )
    ):
        if task.rq_job_id:
            cancel_and_delete_task(task.rq_job_id)
        executions = Execution.objects.filter(
            task=task,
            status__in=[Status.REQUESTED, Status.RUNNING]
        ).all()
        for execution in executions:
            if execution.rq_job_id:
                cancel_job(execution.rq_job_id)
            if execution.rq_job_pid:
                os.kill(execution.rq_job_pid, signal.SIGKILL)
            execution.status = Status.CANCELLED
            execution.end = timezone.now()
            execution.save()
        task.status = Status.CANCELLED
        task.end = timezone.now()
        task.save()
    else:
        raise ValidationError({'id': f'Task {task.id} can not be cancelled'})
