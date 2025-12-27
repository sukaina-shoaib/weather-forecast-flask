from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, user_id, message):
        """Receive alert update"""
        pass
