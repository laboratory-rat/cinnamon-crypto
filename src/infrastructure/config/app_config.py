from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    name: str

    @property
    def connection_string(self):
        return f'sqlite:///{self.name}'


class NNSettings(BaseSettings):
    path: str


class AppConfig(BaseSettings):
    api_key: str
    api_secret: str
    api_client_test: bool = False

    database: DBSettings
    nn: NNSettings

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'
