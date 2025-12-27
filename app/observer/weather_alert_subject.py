class WeatherAlertSubject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, user_id, message):
        for observer in self.observers:
            try:
                observer.update(user_id, message)
            except Exception as e:
                print(f"[OBS-FAIL] {observer.__class__.__name__}: {e}")