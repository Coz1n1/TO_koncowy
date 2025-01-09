class Observer:
    def update(self, message):
        raise NotImplementedError("Subclass must implement abstract method")

class Observable:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, message):
        for obs in self._observers:
            obs.update(message)
