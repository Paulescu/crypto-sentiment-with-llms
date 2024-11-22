from pydantic_settings import BaseSettings, SettingsConfigDict

class AnthropicConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='anthropic.env', env_file_encoding='utf-8')
    api_key: str
    model_name: str = "claude-3-opus-20240229"
    max_tokens: int = 300

anthropic_config = AnthropicConfig()