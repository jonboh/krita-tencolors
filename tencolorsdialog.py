# SPDX-License-Identifier: CC0-1.0

from PyQt5.QtWidgets import QDialog


class TenColorsDialog(QDialog):
    def __init__(self, uitencolors, parent=None):
        super(TenColorsDialog, self).__init__(parent)

        self.uitencolors = uitencolors

    def accept(self):
        self.uitencolors.tencolors.writeSettings()

        super(TenColorsDialog, self).accept()

    def closeEvent(self, event):
        event.accept()
