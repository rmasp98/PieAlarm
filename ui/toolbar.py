
from PyQt5.QtWidgets import QLabel, QToolBar, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap

import ui.controller

class ToolBar(QToolBar):

    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)
        self.setMaximumHeight(50)

        layout = QHBoxLayout()
        tb_widget = QWidget()
        tb_widget.setLayout(layout)

        layout.addWidget(BackButton())
        layout.addStretch()
        layout.addWidget(SaveButton())
        layout.addWidget(DeleteButton())
        layout.setContentsMargins(0, 0, 0, 0)

        self.setMovable(False)
        self.addWidget(tb_widget)

        self.enable_edit(False)

    def enable_edit(self, enable, save_event=None, delete_event=None):
        if enable:
            self.findChild(SaveButton).show()
            self.findChild(SaveButton).mouseReleaseEvent = save_event
            self.findChild(DeleteButton).show()
            self.findChild(DeleteButton).mouseReleaseEvent = delete_event
        else:
            self.findChild(SaveButton).hide()
            self.findChild(DeleteButton).hide()


class BackButton(QLabel):

    def __init__(self, parent=None):
        super(BackButton, self).__init__(parent)
        pixmap = QPixmap("ui/icons/back.png")
        self.setPixmap(pixmap.scaledToWidth(40))
        self.mouseReleaseEvent = _back_event

def _back_event(_):
    ui.controller.UiController().set_screen("back")

class SaveButton(QLabel):

    def __init__(self, parent=None):
        super(SaveButton, self).__init__(parent)
        pixmap = QPixmap("ui/icons/save.png")
        self.setPixmap(pixmap.scaledToWidth(30))

class DeleteButton(QLabel):

    def __init__(self, parent=None):
        super(DeleteButton, self).__init__(parent)
        pixmap = QPixmap("ui/icons/delete.png")
        self.setPixmap(pixmap.scaledToWidth(30))
