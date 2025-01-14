from enum import Enum


class Status(Enum):
    RUNNING = "RUNNING"
    CLEARED = "CLEARED"


class AppState:
    _instance = None
    status: Status
    details: dict

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.status = Status.RUNNING
        self.details = {}

    def set_status(self, new_status: Status):
        self.status = new_status

    def get_status(self) -> Status:
        return self.status

    def set_detail(self, key: str, value: any):
        self.details[key] = value

    def get_detail(self, key: str) -> any:
        return self.details.get(key, None)
