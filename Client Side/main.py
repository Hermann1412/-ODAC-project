from PyQt5.QtWidgets import QApplication
import sys
from login_window import LoginWindow

# Create a QApplication instance, which manages the GUI application's control flow
app = QApplication(sys.argv)

# Create an instance of LoginWindow, which represents the main window of the application
mainwindow = LoginWindow()

# Execute the application's event loop
try:
  # Start the application's event loop and wait for the app to exit
  sys.exit(app.exec_())
except:
  print("Existing")