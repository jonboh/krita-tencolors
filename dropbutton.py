# SPDX-License-Identifier: CC0-1.0

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QPushButton


class DropButton(QPushButton):
    def __init__(self, parent):
        super(DropButton, self).__init__(parent)

        self.colorChooser = None

        self.color = None
        self.setFixedSize(64, 64)
        self.setIconSize(QSize(64, 64))

    def selectColor(self):
        view = Application.activeWindow().activeView()
        color = view.foregroundColor()
        if color:
            qcolor = color.colorForCanvas(view.canvas())
            color_image = QImage(64, 64, QImage.Format.Format_RGB444)
            color_image.fill(qcolor)
            self.color = qcolor
            self.setIcon(QIcon(QPixmap.fromImage(color_image)))
            view.showFloatingMessage(
                str(i18n("Color set")),
                QIcon(QPixmap.fromImage(color_image)),
                1000,
                1,
            )
