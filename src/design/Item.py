class Item:
    def __init__(self, number: str, description: str, model: str, manufacturer: str, room: str, last_service: str, serial: str):
        self._number = number
        self._description = description
        self._model = model
        self._manufacturer = manufacturer
        self._room = room
        self._last_service = last_service
        self._serial = serial

    @property
    def number(self) -> str:
        return self._number

    @property
    def description(self) -> str:
        return self._description
    
    @property
    def model(self) -> str:
        return self._model

    def __str__(self) -> str:
        return f"{self._number} - {self._description}"

    def full_info(self) -> str:
        return f"{str(self)}\nModel: {self._model}\nManufacturer: {self._manufacturer}\nRoom: {self._room}\nLast Service: {self._last_service}\nSerial: {self._serial}"

    def __hash__(self) -> int:
        return hash(self._number)
