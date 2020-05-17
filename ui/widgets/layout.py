import PyQt5.QtWidgets


def create_horizontal_layout(widget, parent=None):
    return _create_layout(PyQt5.QtWidgets.QHBoxLayout(), widget, parent)


def create_vertical_layout(widget, parent=None):
    return _create_layout(PyQt5.QtWidgets.QVBoxLayout(), widget, parent)


def create_grid_layout(widget, parent=None):
    return _create_layout(PyQt5.QtWidgets.QGridLayout(), widget, parent)


def create_spacer():
    return PyQt5.QtWidgets.QSpacerItem(
        0,
        0,
        PyQt5.QtWidgets.QSizePolicy.MinimumExpanding,
        PyQt5.QtWidgets.QSizePolicy.MinimumExpanding,
    )


def _create_layout(layout, widget, parent):
    widget.setLayout(layout)
    if parent is not None:
        parent.addWidget(widget)
    return layout
