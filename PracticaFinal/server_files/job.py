from typing import List


class Job():
    """ Brief description of Job class..."""
    def __init__(self, client_id: int, job_type: str, payload: List) -> None:
        # Client Identificator
        self.client_id = client_id
        # Sets the type of the job
        self.job_type = job_type
        # The payload contains the data to process
        self.payload = payload
        # Flag of done job is initialized to zero
        self.done = False