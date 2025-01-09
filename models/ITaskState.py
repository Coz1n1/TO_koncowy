from abc import ABC, abstractmethod

class TaskState(ABC):
    @abstractmethod
    def move_to_next(self, task):
        pass

    @abstractmethod
    def move_to_previous(self, task):
        pass

    @abstractmethod
    def get_status(self):
        pass
