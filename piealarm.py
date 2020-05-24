import logging
import logging.handlers
import os

import PyQt5.QtWidgets

import ui
import ui.window
import alarm.manager
import weather.weather
import weather.darksky
import settings.interface
import sound.player

import PyQt5.QtCore


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
        # w.start_api_poll()
        s = settings.interface.Interface()
        p = sound.player.Player()
        ui.Ctrl().init(
            PyQt5.QtWidgets.QApplication([os.sys.argv]),
            ui.window.Window(),
            alarm.manager.Manager(s),
            w,
            p,
            s,
        )
        ui.Ctrl().exec(screen=ui.Screen.PLAYER, theme="dark")
        # ui.Ctrl().exec(theme="dark")
    except Exception as e:
        logging.exception("Exception in main()")
        print(e)
        exit(1)
