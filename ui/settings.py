import PyQt5.QtWidgets

from ui.widgets.layout import create_vertical_layout
from ui.widgets.layout import create_horizontal_layout
from ui.keyboard import LineEdit
from ui.widgets.toggle import ToggleSwitch
from ui.widgets.spinner import Spinner
from ui.widgets.text import Text, FontSize
import ui
from scheduler.observer import Observer


class SettingsScreen(PyQt5.QtWidgets.QWidget):
    def __init__(self, settings, parent=None):
        super(SettingsScreen, self).__init__(parent)
        ui.Ctrl().enable_toolbar_action("save", True, event=self._save)

        self._settings = settings
        self._settings_dict = self._create_settings_dict(settings)
        self._create_layout()

    def _create_layout(self):
        screen_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        self._scroll = PyQt5.QtWidgets.QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAlwaysOff)
        self._scroll.setHorizontalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAlwaysOff)
        screen_layout.addWidget(self._scroll)

        form_widget = PyQt5.QtWidgets.QGroupBox()
        self._scroll.setWidget(form_widget)
        form_layout = PyQt5.QtWidgets.QFormLayout(form_widget)
        form_layout.setSpacing(50)
        for package in self._settings_dict:
            form_layout.addRow(Text(package, FontSize.MEDIUM))
            for name, setting_widget in self._settings_dict[package].items():
                form_layout.addRow(Text(name, FontSize.SMALL), setting_widget)

    def _create_settings_dict(self, settings):
        new_settings = {}
        for package in settings.list_packages():
            new_settings[package] = {}
            for name, value in settings.get_settings(package).items():
                options = settings.get_setting_options(package, name)
                if options.o_type == "select":
                    new_settings[package][name] = SelectSetting(value, options.options)
                elif options.o_type == "text":
                    new_settings[package][name] = TextSetting(value)
                    new_settings[package][name].connect(self._move_scroll)
                elif options.o_type == "toggle":
                    new_settings[package][name] = ToggleSetting(value)
                elif options.o_type == "colour":
                    new_settings[package][name] = ColourSetting(value)
        return new_settings

    def _move_scroll(self, y_pos):
        scroll_y_pos = self.mapToGlobal(PyQt5.QtCore.QPoint(0, 0)).y()
        vbar_pos = self._scroll.verticalScrollBar().value()
        new_vbar_pos = vbar_pos + (y_pos - scroll_y_pos)
        # currently may be above screen so if not at bottom then scroll up
        if new_vbar_pos < self._scroll.verticalScrollBar().maximum() - 50:
            new_vbar_pos -= 50
        self._scroll.verticalScrollBar().setValue(new_vbar_pos)

    def _save(self):
        try:
            for package in self._settings_dict:
                for name, setting in self._settings_dict[package].items():
                    self._settings.update_setting(package, name, setting.get_value())
            self._settings.save()
            _save_message()
        except Exception as err:
            _save_message(str(err))


class TextSetting(LineEdit):
    def __init__(self, label="", parent=None):
        super(TextSetting, self).__init__(label, parent)
        self._signal = Observer()

    def get_value(self):
        return self.text()

    def connect(self, function):
        self._signal.subscribe(function)

    def focusInEvent(self, e):
        super(TextSetting, self).focusInEvent(e)
        self._signal.notify(self.mapToGlobal(PyQt5.QtCore.QPoint(0, 0)).y())


class SelectSetting(Spinner):
    def __init__(self, value, options, loop=False, underhang=True, parent=None):
        select_options = [str(i) for i in options]
        index = select_options.index(str(value))
        self._type = type(value)
        super(SelectSetting, self).__init__(
            select_options, index, loop, underhang, parent
        )

    def get_value(self):
        return self._type(super(SelectSetting, self).get_value())


class ToggleSetting(ToggleSwitch):
    def get_value(self):
        return self.is_active()


class ColourSetting(PyQt5.QtWidgets.QWidget):
    def __init__(self, value, parent=None):
        super(ColourSetting, self).__init__(parent)
        layout = create_horizontal_layout(self)
        options = [str(i) for i in range(256)]
        self._spinners = [
            Spinner(options, value[0], False),
            Spinner(options, value[1], False),
            Spinner(options, value[2], False),
        ]
        layout.addWidget(self._spinners[0])
        layout.addWidget(self._spinners[1])
        layout.addWidget(self._spinners[2])

    def get_value(self):
        return [
            int(self._spinners[0].get_value()),
            int(self._spinners[1].get_value()),
            int(self._spinners[2].get_value()),
        ]


def _save_message(message=""):
    msg = PyQt5.QtWidgets.QMessageBox()
    if message == "":
        msg.setIcon(PyQt5.QtWidgets.QMessageBox.Information)
        msg.setText("Settings have been saved")
    else:
        msg.setIcon(PyQt5.QtWidgets.QMessageBox.Warning)
        msg.setText(message)
    msg.setStandardButtons(PyQt5.QtWidgets.QMessageBox.Ok)
    msg.exec_()
