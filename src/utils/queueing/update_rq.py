from rq import get_current_job


def update_job_status(progress: str, message: str) -> None:
    """
    Update the status of the current job.
    If the job is not found, do nothing.

    Args:
        progress (str): The progress status of the job.
        message (str): The message to display for the job.

    Returns:
        None
    """
    rq_job = get_current_job()
    if not rq_job:
        return
    rq_job.meta["progress"] = progress
    rq_job.meta["message"] = message
    rq_job.save_meta()
