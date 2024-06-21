from enum import Enum
from dataclasses import dataclass, field


class Location(Enum):
    RUSSIA = "В России"
    WORLD = "За рубежом"
    NO_MATTER = "Не имеет значения"


class Condition(Enum):
    EX = "Б / У"
    NEW = "Новый"
    NO_MATTER = "Не имеет значения"


@dataclass
class FindForm:
    name: str = ""
    size: str = ""
    photos_ids: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    condition: Condition = Condition.NEW
    location: Location = Location.WORLD

    def set_condition(self, text):
        if text == "Новое":
            self.condition = Condition.NEW
        elif text == "Б \\ У":
            self.condition = Condition.EX
        elif text == "Не имеет значения":
            self.condition = Condition.NO_MATTER
        else:
            raise ValueError(f"Неизвестный тип состояния вещи: {self.condition}")

    def set_location(self, text):
        if text == "В России":
            self.location = Location.RUSSIA
        elif text == "За рубежом":
            self.location = Location.WORLD
        elif text == "Не имеет значения":
            self.location = Location.NO_MATTER
        else:
            raise ValueError(f"Неизвестный тип локации: {self.location}")


@dataclass
class Find:
    id: int
    client_id: int
    cost: int
    is_confirm: bool
