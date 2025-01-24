import threading

class EmailManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._email = None
        return cls._instance

    def save_email(self, email):
        self._email = email

    def get_email(self):
        return self._email

email_manager = EmailManager()