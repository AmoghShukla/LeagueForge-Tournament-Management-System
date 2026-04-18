import enum

class UserRole(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    VENUE_MANAGER = "VENUE_MANAGER"
    SCORE_UPDATER = "SCORE_UPDATER"
    TEAM_OWNER = "TEAM_OWNER"

class MatchStatus(enum.Enum):
    STARTED = "STARTED"
    ABANDONED = "ABANDONED"
    IN_PROGRESS = "IN_PROGRESS"
    YET_TO_START = "YET_TO_START"

class ResultType(enum.Enum):
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"

class TossDecision(enum.Enum):
    BATTING = "BATTING"
    FIELDING = "FIELDING"