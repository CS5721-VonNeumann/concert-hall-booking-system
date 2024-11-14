class Subject():
    """
    The Subject class holds a list of observers and notifies them when there is a state change.
    """
    def __init__(self):
        self._observers = []

    def attach(self, observer, interest):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, interest, message):
        raise NotImplementedError("Subclasses should implement this method")


class Observer():
    """
    The Observer class defines the method that will be called to update the observer when the subject changes.
    """
    def update(self, message):
        raise NotImplementedError("Subclasses should implement this method")
