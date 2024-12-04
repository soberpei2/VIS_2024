# from __future__ import annotations

# import argparse
# import pandas as pd

# funktion zum einlesen der Daten
# def read_data(fname):
#     return pd.read_csv(fname)

# C:\Users\126al\AppData\Local\Programs\Python\Python312\python.exe Tutorial\main.py -f Tutorial\all_day.csv

# if __name__ == "__main__":
#     options = argparse.ArgumentParser()
#     options.add_argument("-f", "--file", type=str, required=True)
#     args = options.parse_args()
#     data = read_data(args.file)
#     print(data)
#____________________________________________

# from __future__ import annotations

# import argparse
# import pandas as pd

# from PySide6.QtCore import QDateTime, QTimeZone

# # datum anpassen
# def transform_date(utc, timezone=None):
#     utc_fmt = "yyyy-MM-ddTHH:mm:ss.zzzZ"
#     new_date = QDateTime().fromString(utc, utc_fmt)
#     if timezone:
#         new_date.setTimeZone(timezone)
#     return new_date


# def read_data(fname):
#     # Read the CSV content
#     df = pd.read_csv(fname)

#     # Remove wrong magnitudes
#     df = df.drop(df[df.mag < 0].index)
#     magnitudes = df["mag"]

#     # My local timezone
#     timezone = QTimeZone(b"Europe/Berlin")

#     # Get timestamp transformed to our timezone
#     times = df["time"].apply(lambda x: transform_date(x, timezone))

#     return times, magnitudes


# if __name__ == "__main__":
#     options = argparse.ArgumentParser()
#     options.add_argument("-f", "--file", type=str, required=True)
#     args = options.parse_args()
#     data = read_data(args.file)
#     print(data)
# ##____________________________________________________________________________________

# from PySide6.QtCore import Slot
# from PySide6.QtGui import QAction, QKeySequence
# from PySide6.QtWidgets import QMainWindow

# class MainWindow(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.setWindowTitle("Eartquakes information")

#         # Menu
#         self.menu = self.menuBar()
#         self.file_menu = self.menu.addMenu("File")

#         # Exit QAction
#         exit_action = QAction("Exit", self)
#         exit_action.setShortcut(QKeySequence.Quit)
#         exit_action.triggered.connect(self.close)

#         self.file_menu.addAction(exit_action)

#         # Status Bar
#         self.status = self.statusBar()
#         self.status.showMessage("Data loaded and plotted")

#         # Window dimensions
#         geometry = self.screen().availableGeometry()
#         self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

# #____________________________________________

from __future__ import annotations

import sys
import argparse
import pandas as pd

from PySide6.QtCore import QDateTime, QTimeZone
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from main_widget import Widget


def transform_date(utc, timezone=None):
    utc_fmt = "yyyy-MM-ddTHH:mm:ss.zzzZ"
    new_date = QDateTime().fromString(utc, utc_fmt)
    if timezone:
        new_date.setTimeZone(timezone)
    return new_date


def read_data(fname):
    # Read the CSV content
    df = pd.read_csv(fname)

    # Remove wrong magnitudes
    df = df.drop(df[df.mag < 0].index)
    magnitudes = df["mag"]

    # My local timezone
    timezone = QTimeZone(b"Europe/Berlin")

    # Get timestamp transformed to our timezone
    times = df["time"].apply(lambda x: transform_date(x, timezone))

    return times, magnitudes


if __name__ == "__main__":
    options = argparse.ArgumentParser()
    options.add_argument("-f", "--file", type=str, required=True)
    args = options.parse_args()
    data = read_data(args.file)

    # Qt Application
    app = QApplication(sys.argv)

    widget = Widget(data)
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec())

