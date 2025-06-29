from core.config import conf
from core.server import GunicornApplication, get_application_options

from main import app as main_app


def main():
    app = GunicornApplication(
        application=main_app,
        options=get_application_options(
            bind=conf.server.bind,
            workers=conf.server.workers,
            timeout=conf.server.timeout,
            log_level=conf.log.log_level,
        ),
    )
    app.run()


if __name__ == "__main__":
    main()
