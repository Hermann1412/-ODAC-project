from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from detection import Detection  # Your detection thread class

# Manages the detection window and detection thread
class DetectionWindow(QMainWindow):
    def __init__(self, parent=None):
        super(DetectionWindow, self).__init__()
        loadUi('UI/detection_window.ui', self)
        self.parent = parent  # Reference to settings window
        self.stop_detection_button.clicked.connect(self.stop_monitoring)

    # Create and store the detection thread instance
    def create_detection_instance(self, token, location, receiver):
        self.detection = Detection(token, location, receiver)

    # Display frame updates on the UI label
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label_detection.setPixmap(QPixmap.fromImage(image))

    # Start detection and show detection window
    def start_detection(self):
        self.detection.changePixmap.connect(self.setImage)
        self.detection.start()
        self.show()

    # Stop monitoring, hide detection window, return to settings window
    def stop_monitoring(self):
        self.detection.running = False
        self.hide()
        if self.parent:
            self.parent.show()

    # If detection window is closed directly
    def closeEvent(self, event):
        self.detection.running = False
        if self.parent:
            self.parent.show()
        event.accept()
