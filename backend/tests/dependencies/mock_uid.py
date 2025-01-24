import threading

class UIDManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._uid = None
        return cls._instance

    def save_uid(self, uid):
        self._uid = uid

    def get_uid(self):
        return self._uid
    
    def reset_uid(self):
        self._uid = None

uid_manager = UIDManager()