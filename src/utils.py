from datetime import datetime
from typing import List

from firebase_admin import db

from settings import firebase_settings


def _get_now_timestamp() -> int:
    return int(datetime.utcnow().timestamp() * 1000)


def init_quiz_info(quiz_id: str, quiz_title: str, quiz_emoji: str):
    app_name = firebase_settings.app_name
    db.reference(f"{app_name}/{quiz_id}").update({"title": quiz_title, "emoji": quiz_emoji})


def save_user_to_leaderboard(quiz_id: str, user_name: str):
    app_name = firebase_settings.app_name
    db.reference(f"{app_name}/{quiz_id}/leaderboard/{user_name}").update({"answer_time": _get_now_timestamp()})


def get_leaderboard(quiz_id: str) -> List[str]:
    app_name = firebase_settings.app_name
    leaderboard = db.reference(f"{app_name}/{quiz_id}/leaderboard").get()

    if leaderboard is None:
        return None

    leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]["answer_time"])[:10]
    leaderboard = [v[0] for v in leaderboard]

    return leaderboard
