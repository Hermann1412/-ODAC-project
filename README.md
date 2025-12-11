# ODAC-project


This project implements an AI-assisted object detection system designed to enhance safety in educational environments. Using Python, YOLO, OpenCV, TensorFlow, and a Django + SQL backend, the system detects and classifies objects in real time—such as bags, bottles, electronic devices, and potential hazards (e.g., knives, scissors). Data is automatically logged and connected to registered student profiles for administrative monitoring and analysis.

🚀 Key Features
Real-Time Object Detection

Uses YOLO, OpenCV, TensorFlow, and PyTorch (YOLOv5/YOLOv8)

Identifies objects from camera input

Displays bounding boxes and confidence scores

Supports real-time detection or image/video upload analysis

Backend & Database Integration

Built using Django ORM

Compatible with SQLite and PostgreSQL

Stores:

Detected objects

Timestamps

User IDs (person carrying the object)

Detection metadata

Designed as a relational structure linking objects ↔ users

Graphical User Interface (GUI)

Developed using HTML, CSS, JavaScript, Django templates

Features:

Live camera feed with detections

Image/video upload

Detection logs and confidence scores

Search & filter tools (e.g., items detected per month)

Real-time alerts when dangerous objects appear

Alerting System

Generates notifications for detected threats

Includes: object, timestamp, user, and location

Automatically logs events for later analysis

🧠 Educational Purpose

This project was created as a capstone / senior-year engineering project.
It teaches students how to integrate concepts from:

Machine learning & computer vision

Software engineering

Database design

Front-end development

Ethical and security considerations in AI

It demonstrates the value of project-based learning and provides experience with real-world AI systems.

📈 Results

Successfully detects objects in real time

Provides accurate bounding boxes and classification

Stores all detection records and supports historical queries

Includes a functional admin dashboard for monitoring


Technologies Used
Category	Tools / Libraries
Object Detection	YOLOv5/YOLOv8, TensorFlow Object Detection API, OpenCV
Backend	Django, Django ORM
Database	SQLite / PostgreSQL
Frontend	HTML, CSS, JavaScript, Django Templates
GUI Libraries	Tkinter, PyQt (optional components)
Hardware	USB camera or CCTV feed
