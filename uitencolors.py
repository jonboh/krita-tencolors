# SPDX-License-Identifier: CC0-1.0

import krita
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QDialogButtonBox, QHBoxLayout, QLabel, QVBoxLayout

from . import dropbutton, tencolorsdialog


class UITenColors(object):
    def __init__(self):
        self.kritaInstance = krita.Krita.instance()
        self.mainDialog = tencolorsdialog.TenColorsDialog(
            self, self.kritaInstance.activeWindow().qwindow()
        )

        self.buttonBox = QDialogButtonBox(self.mainDialog)
        self.vbox = QVBoxLayout(self.mainDialog)
        self.hbox = QHBoxLayout(self.mainDialog)

        self.buttonBox.accepted.connect(self.mainDialog.accept)
        self.buttonBox.rejected.connect(self.mainDialog.reject)

        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

    def initialize(self, tencolors):
        self.tencolors = tencolors

        self.loadButtons()

        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(
            QLabel(
                i18n(
                    "Select the color, then click on the button "
                    "you want to use to select it."
                )
            )
        )
        self.vbox.addWidget(
            QLabel(
                i18n(
                    "Shortcuts are configurable through the <i>Keyboard Shortcuts</i> "
                    "interface in Krita's settings."
                )
            )
        )

        self.vbox.addWidget(self.buttonBox)

        self.mainDialog.show()
        self.mainDialog.activateWindow()
        self.mainDialog.exec_()

    def loadButtons(self):
        self.tencolors.buttons = []

        for index, item in enumerate(
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        ):
            buttonLayout = QVBoxLayout()
            button = dropbutton.DropButton(self.mainDialog)
            button.setObjectName(item)
            button.clicked.connect(button.selectColor)

            action = self.tencolors.actions[index]

            if action and action.color:
                button.color = action.color
                qcolor = action.color
                color_image = QImage(64, 64, QImage.Format.Format_RGB444)
                color_image.fill(qcolor)
                button.setIcon(QIcon(QPixmap.fromImage(color_image)))

            buttonLayout.addWidget(button)

            label = QLabel(action.shortcut().toString())
            label.setAlignment(Qt.AlignHCenter)
            buttonLayout.addWidget(label)

            self.hbox.addLayout(buttonLayout)
            self.tencolors.buttons.append(button)
