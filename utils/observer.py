class Observer:
    def __init__(self):
        self._observers = set()

    def subscribe(self, callback):
        if callable(callback):
            self._observers.add(callback)
        else:
            raise ValueError("Callback must be a callable object")

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            try:
                observer(*args, **kwargs)
            except TypeError:
                raise ValueError(
                    "Subscriber has not provided a function "
                    "with correct number of arguments. Please check "
                    "notifier to determine what is expected"
                )
