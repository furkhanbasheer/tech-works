# main.py
import sys
import os
import cv2
import csv
import time
import datetime
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont

# ---------- Utils ----------
def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# ---------- Attendance Logic ----------
def take_images(name, roll_no):
    assure_path_exists("TrainingImage")
    cam = cv2.VideoCapture(0)
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    sampleNum = 0

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleNum += 1
            cv2.imwrite(f"TrainingImage/{name}.{roll_no}.{sampleNum}.jpg",
                        gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
        cv2.imshow('Taking Images', img)
        if cv2.waitKey(1) == ord('q') or sampleNum >= 50:
            break
    cam.release()
    cv2.destroyAllWindows()
    print(f"Images captured for {name}")

# ---------- Main Window ----------
class AttendanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Attendance System")
        self.setGeometry(50, 50, 900, 600)
        self.setStyleSheet("background-color: black; color: white;")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Top - Clock & Take Attendance
        top_layout = QHBoxLayout()
        self.clock_label = QLabel(time.strftime('%I:%M:%S %p'))
        self.clock_label.setFont(QFont("Comic Sans MS", 20, QFont.Bold))
        self.clock_label.setAlignment(Qt.AlignLeft)

        self.attendance_btn = QPushButton("Take Attendance")
        self.attendance_btn.setFont(QFont("Comic Sans MS", 14, QFont.Bold))
        self.attendance_btn.setStyleSheet("background-color: white; color: black;")
        self.attendance_btn.clicked.connect(self.track_attendance)

        top_layout.addWidget(self.clock_label)
        top_layout.addStretch()
        top_layout.addWidget(self.attendance_btn)
        main_layout.addLayout(top_layout)

        # Middle - Tiles Layout for Registration
        self.tiles_layout = QHBoxLayout()
        main_layout.addLayout(self.tiles_layout)
        self.add_registration_tile("New User")

        # Bottom - Attendance Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Time"])
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        # Clock update
        self.update_clock()

    def update_clock(self):
        self.clock_label.setText(time.strftime('%I:%M:%S %p'))
        QTimer.singleShot(1000, self.update_clock)

    def add_registration_tile(self, title):
        tile = QLabel(title)
        tile.setFont(QFont("Comic Sans MS", 16, QFont.Bold))
        tile.setAlignment(Qt.AlignCenter)
        tile.setFixedSize(180, 100)
        tile.setStyleSheet("background-color: white; color: black; border-radius: 10px;")
        self.tiles_layout.addWidget(tile)

        # Animation - slide in
        effect = QGraphicsOpacityEffect()
        tile.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(1500)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.start()

    def track_attendance(self):
        print("Starting attendance... (simulate real-time capture)")
        # Here you can integrate LBPHFaceRecognizer logic

if __name__ == "__main__":
    from PyQt5.QtCore import QTimer
    app = QApplication(sys.argv)
    window = AttendanceApp()
    window.show()
    sys.exit(app.exec_())
