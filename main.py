from PyQt5.QtWidgets import QApplication
import sys
from GUI.start_screen import MainWindow 

def main():
    """
    Main function that initializes the application and starts the main window.
    """
    app = QApplication(sys.argv)
    main_window = MainWindow()  
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
