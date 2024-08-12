from settings import ADMIN_PORT, ADMIN_HOST
from settings.development import HOT_RELOAD
from apps.admin import app


if __name__ == "__main__":
    app.run(host=ADMIN_HOST, port=ADMIN_PORT, debug=HOT_RELOAD)
