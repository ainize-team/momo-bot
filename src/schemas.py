from typing import List

from pydantic import BaseModel


class LeaderboardRecord(BaseModel):
    user_id: str
    num_attempt_quiz: int
    num_solved_quiz: int


class Leaderboard(BaseModel):
    records: List[LeaderboardRecord]
