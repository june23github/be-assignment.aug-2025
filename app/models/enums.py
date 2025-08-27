import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"

class TaskStatus(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

class TaskPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
