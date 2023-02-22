from PyQt6.QtWidgets import QApplication
from view.ui import Ui
import sys


def main():
    app = QApplication(sys.argv)
    window = Ui()
    app.exec()


if __name__ == "__main__":
    main()






