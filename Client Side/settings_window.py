from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from detection_window import DetectionWindow

# Manages the settings window
class SettingsWindow(QMainWindow):
    def __init__(self, token):
        super(SettingsWindow, self).__init__()
        loadUi('UI/settings_window.ui', self)

        self.token = token
        self.detection_window = None

        # Connect the start button (change pushButton to your actual button object name if different)
        self.pushButton.clicked.connect(self.go_to_detection)

        # Popup message in case of empty fields
        self.popup = QMessageBox()
        self.popup.setWindowTitle("Failed")
        self.popup.setText("Fields must not be empty.")

    def displayInfo(self):
        self.show()

    # Called when "Start Monitoring" button is clicked
    def go_to_detection(self):
        location = self.location_input.text()
        receiver = self.sendTo_input.text()

        if location == '' or receiver == '':
            self.popup.exec_()
        else:
            # If detection window already exists and is open, do nothing
            if self.detection_window and self.detection_window.isVisible():
                print('Detection window is already open!')
            else:
                # Create and show detection window with self as parent
                self.detection_window = DetectionWindow(parent=self)
                self.detection_window.create_detection_instance(self.token, location, receiver)
                self.detection_window.start_detection()
                self.hide()  # Hide settings window during detection

    # When settings window is closed
    def closeEvent(self, event):
        if self.detection_window and self.detection_window.isVisible():
            self.detection_window.detection.running = False
            self.detection_window.close()
        event.accept()
