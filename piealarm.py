import logging
import logging.handlers
import os

import PyQt5.QtWidgets

import ui
import ui.window
import alarm.manager
import weather.weather
import weather.darksky


def setup_logging():
    handler = logging.handlers.WatchedFileHandler(
        os.environ.get("LOGFILE", "piealarm.log")
    )
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)


if __name__ == "__main__":
    setup_logging()
    try:
        w = weather.weather.Weather(weather.darksky.Darksky())
        w.start_api_poll()
        ui.Ctrl().init(
            PyQt5.QtWidgets.QApplication([]),
            ui.window.Window(),
            alarm.manager.Manager(),
            w,
        )
        # ui.Ctrl().exec(screen=ui.Screen.VIEW, theme="dark")
        ui.Ctrl().exec(theme="dark")
    except:
        logging.exception("Exception in main()")
        exit(1)
