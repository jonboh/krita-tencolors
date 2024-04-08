# SPDX-License-Identifier: CC0-1.0

import krita
from PyQt5.QtGui import QColor, QIcon, QImage, QPixmap

from . import uitencolors


def str2color(string_color: str) -> QColor:
    if string_color == "None":
        return None
    else:
        try:
            red, green, blue, alpha = string_color.split(" ")
            return QColor(int(red), int(green), int(blue), int(alpha))
        except:
            return None


def color2str(color: QColor) -> str:
    if color:
        return f"{color.red()} {color.green()} {color.blue()} {color.alpha()}"
    else:
        return "None"


class TenColorsExtension(krita.Extension):
    def __init__(self, parent):
        super(TenColorsExtension, self).__init__(parent)

        self.actions = []
        self.buttons = []
        self.selectedColors = []
        # Indicates whether we want to activate the previous-selected color
        # on the second press of the shortcut
        # Indicates whether we want to select the freehand color tool
        # on the press of a color shortcut
        self.oldColor = None

    def setup(self):
        self.readSettings()

    def createActions(self, window):
        action = window.createAction("ten_colors", i18n("Ten Colors"))
        action.setToolTip(i18n("Assign ten color to ten shortcuts."))
        action.triggered.connect(self.initialize)
        self.loadActions(window)

    def initialize(self):
        self.uitencolors = uitencolors.UITenColors()
        self.uitencolors.initialize(self)

    def readSettings(self):
        string_colors = Application.readSetting("", "tencolors", "").split(",")
        self.selectedColors = list(map(str2color, string_colors))

    def writeSettings(self):
        colors = []

        for index, button in enumerate(self.buttons):
            self.actions[index].color = button.color
            colors.append(button.color)

        Application.writeSetting("", "tencolors", ",".join(map(color2str, colors)))

    def loadActions(self, window):
        for index, item in enumerate(
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        ):
            action = window.createAction(
                "activate_color_" + item,
                str(i18n("Activate Color {num}")).format(num=item),
                "",
            )
            action.triggered.connect(self.activateColor)

            action.color = None

            # in Krita 4.x we used to replace spaces in preset names with
            # underscores, which has changed in Krita 5.x. Here we just
            # try hard to load the legacy preset

            if index < len(self.selectedColors):
                action.color = self.selectedColors[index]
            self.actions.append(action)

    def activateColor(self):
        qcolor = self.sender().color
        if qcolor:
            window = Application.activeWindow()
            color = window.activeView().foregroundColor().fromQColor(qcolor)
            if color:
                if window and len(window.views()) > 0:
                    window.activeView().setForeGroundColor(color)

                color_image = QImage(64, 64, QImage.Format.Format_RGB444)
                color_image.fill(qcolor)
                window.activeView().showFloatingMessage(
                    str(i18n("Color selected")),
                    QIcon(QPixmap.fromImage(color_image)),
                    1000,
                    1,
                )
