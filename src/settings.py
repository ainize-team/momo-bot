from pydantic import BaseSettings, Field


class DiscordSettings(BaseSettings):
    token: str = Field(..., description="Discord Bot Token")
    guild_id: str = Field(..., description="Discord Guild ID")


class FirebaseSettings(BaseSettings):
    app_name: str = Field(default="momo", description="Firebase App Name")
    cred_path: str = Field(default="/app/key/serviceAccountKey.json", description="Firebase Credential JSON File Path")
    database_url: str = Field(..., description="Firebase Realtime Database URL")


discord_settings = DiscordSettings()
firebase_settings = FirebaseSettings()
