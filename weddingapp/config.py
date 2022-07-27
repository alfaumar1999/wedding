class BaseConfig:
    SECRET_KEY='Jabs@1999'
    ADMIN_EMAIL='alfaumar@gmail.com'

class TestConfig(BaseConfig):
    ADMIN_EMAIL='basetest@gmail.com'

class LiveConfig(BaseConfig):
    ADMIN_EMAIL='live@gmail.com'