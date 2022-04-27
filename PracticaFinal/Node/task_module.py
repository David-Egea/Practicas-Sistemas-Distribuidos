from abc import ABC, abstractmethod

class taskModule(ABC):
    """ Task ABC module class"""

    def __init__(self, task: str) -> None:
        self.task = task

    @abstractmethod
    def do_task(self) -> None:
        """[Abstract method]: Carries out the module task. """
