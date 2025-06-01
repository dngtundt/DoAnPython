from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Houseware Manager')
        self.setGeometry(100, 100, 800, 600)

        # Create a menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        # Create exit action
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(qApp.quit)
        file_menu.addAction(exit_action)

        # Set the central widget and layout
        self.central_widget = None  # Placeholder for central widget
        self.setCentralWidget(self.central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())