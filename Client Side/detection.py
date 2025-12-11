from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import cv2
import numpy as np
import time
import os
import requests

class Detection(QThread):
    changePixmap = pyqtSignal(QImage)  # Signal for updating the GUI

    def __init__(self, token, location, receiver):
        super(Detection, self).__init__()
        self.token = token
        self.location = location
        self.receiver = receiver
        self.running = True
        self.harmful_objects = {"knife", "fire hydrant", "baseball bat", "wine glass", "scissors", "hair drier"}  # Set of harmful objects
        os.makedirs("saved_frames", exist_ok=True)  # Ensure directory exists
        self.object_counts = {}

    def run(self):
        # Load YOLO model
        net = cv2.dnn.readNet("weights/yolov4.weights", "cfg/yolov4.cfg")

        # Load object classes
        with open("obj.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]

        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
        
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        font = cv2.FONT_HERSHEY_PLAIN

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Unable to open camera.")
            return

        starting_time = time.time()

        while self.running:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                continue

            height, width, channels = frame.shape

            # YOLO processing
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)

            class_ids = []
            confidences = []
            boxes = []
            detected_harmful_objects = []

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    
                    if confidence > 0.5:  # Detection threshold
                        label = str(classes[class_id])
                        if label in self.harmful_objects:
                            detected_harmful_objects.append(label)

                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = confidences[i]
                    color = colors[class_ids[i]]

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), font, 2, color, 2)

            # Save frame if harmful object is detected
            elapsed_time = time.time() - starting_time
            if detected_harmful_objects and elapsed_time >= 10:
                starting_time = time.time()
                self.save_detection(frame, detected_harmful_objects)

            # Convert frame for display in PyQt
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bytesPerLine = channels * width
            convertToQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(854, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

        cap.release()
        cv2.destroyAllWindows()

    def save_detection(self, frame, detected_objects):
        for obj in detected_objects:
            if obj not in self.object_counts:
                self.object_counts[obj] = 1
            else:
                self.object_counts[obj] += 1
            
            filename = f"saved_frames/{obj}_{self.object_counts[obj]}.jpg"
            cv2.imwrite(filename, frame)
            print(f'Frame Saved: {filename}')
            # Store the last saved filename for later use in post_detection
            self.last_saved_frame = filename
            self.post_detection()

    def post_detection(self):
        import requests  # Ensure requests is available (or import at the top of your file)
        try:
            # Ensure a saved detection exists
            if not hasattr(self, 'last_saved_frame'):
                print("No saved detection to post.")
                return
            url = 'https://server-side-deployment-8m3n.onrender.com/api/images/'
            headers = {'Authorization': 'Token ' + self.token}
            with open(self.last_saved_frame, 'rb') as img_file:
                files = {'image': img_file}
                data = {'user_ID': self.token, 'location': self.location, 'alert_receiver': self.receiver}
                response = requests.post(url, files=files, headers=headers, data=data)
            
            if response.ok:
                print('Alert was sent to the server')
            else:
                print('Unable to send alert to the server')
        except Exception as e:
            print('Unable to access server:', e)
