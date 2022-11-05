from .apis import *
from .app import api_v1, app

app.register_blueprint(api_v1)
