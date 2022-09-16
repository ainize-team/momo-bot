# from typing import Dict, List, Union

from firebase_admin import db

from schemas import Leaderboard, LeaderboardRecord
from settings import firebase_settings


app_name = firebase_settings.app_name


def save_quiz_info(quiz_title: str, quiz_emoji: str) -> str:
    reference = db.reference(f"{app_name}/quiz_info").push({"title": quiz_title, "emoji": quiz_emoji})
    quiz_id = reference.key

    return quiz_id


def is_quiz_solved(quiz_id: str, user_id: str) -> bool:
    solved_quiz = db.reference(f"{app_name}/user_info/{user_id}/solved_quiz").get()
    if solved_quiz is None:
        return False

    return quiz_id in solved_quiz


def save_attempt_quiz_info(quiz_id: str, user_id: str):
    attempt_quiz = db.reference(f"{app_name}/user_info/{user_id}/attempt_quiz").get()
    if attempt_quiz is not None:
        if quiz_id in attempt_quiz:
            return
        else:
            num_attempt_quiz = len(attempt_quiz)
    else:
        num_attempt_quiz = 0
    db.reference(f"{app_name}/user_info/{user_id}/attempt_quiz/{num_attempt_quiz}").set(quiz_id)
    db.reference(f"{app_name}/leaderboard/{user_id}/num_attempt_quiz").set(num_attempt_quiz + 1)


def save_solved_quiz_info(quiz_id: str, user_id: str):
    solved_quiz = db.reference(f"{app_name}/user_info/{user_id}/solved_quiz").get()
    if solved_quiz is not None:
        if quiz_id in solved_quiz:
            return
        else:
            num_solved_quiz = len(solved_quiz)
    else:
        num_solved_quiz = 0
    save_attempt_quiz_info(quiz_id, user_id)
    db.reference(f"{app_name}/user_info/{user_id}/solved_quiz/{num_solved_quiz}").set(quiz_id)
    db.reference(f"{app_name}/leaderboard/{user_id}/num_solved_quiz").set(num_solved_quiz + 1)


def get_leaderboard() -> Leaderboard:
    top_n = 10
    leaderboard = db.reference(f"{app_name}/leaderboard").get()

    if leaderboard is None:
        return None

    leaderboard = dict(
        sorted(leaderboard.items(), key=lambda x: (-x[1]["num_solved_quiz"], x[1]["num_attempt_quiz"]))[:top_n]
    )
    leaderboard = Leaderboard(
        records=[
            LeaderboardRecord(
                user_id=user_id,
                num_attempt_quiz=data["num_attempt_quiz"],
                num_solved_quiz=data["num_solved_quiz"],
            )
            for user_id, data in leaderboard.items()
        ]
    )

    return leaderboard
