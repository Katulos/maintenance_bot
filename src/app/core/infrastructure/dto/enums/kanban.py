from enum import Enum


class KanbanState(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    DONE = "done"
