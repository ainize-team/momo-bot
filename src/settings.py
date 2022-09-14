from pydantic import BaseSettings, Field


class DiscordSettings(BaseSettings):
    token: str = Field(..., description="Discord Bot Token")
    guild_id: str = Field(..., description="Discord Guild ID")


class FirebaseCredSettings(BaseSettings):
    type: str = Field(...)
    project_id: str = Field(...)
    private_key_id: str = Field(...)
    private_key: str = Field(...)
    client_email: str = Field(...)
    client_id: str = Field(...)
    auth_uri: str = Field(...)
    token_uri: str = Field(...)
    auth_provider_x509_cert_url: str = Field(...)
    client_x509_cert_url: str = Field(...)


class FirebaseSettings(BaseSettings):
    app_name: str = Field(default="momo", description="Firebase App Name")
    database_url: str = Field(..., description="Firebase Realtime Database URL")


discord_settings = DiscordSettings()
firebase_cred_settings = FirebaseCredSettings()
firebase_settings = FirebaseSettings()
