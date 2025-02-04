import os
import cv2
import torch
import logging
import sqlite3
import pandas as pd
from pathlib import Path
from yolov5 import detect

# Configure Logging
logging.basicConfig(filename="yolo_detection.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Paths
MODEL_PATH = "yolov5s.pt"  # Pre-trained YOLOv5 model
IMAGE_DIR = "images/"  # Directory for input images
OUTPUT_DIR = "detections/"  # Directory for detection results
DB_FILE = "detections.db"  # SQLite Database File
RESULT_CSV = "detection_results.csv"  # CSV file for results

# Step 1: Run YOLOv5 Object Detection
def run_object_detection():
    logging.info("Running YOLOv5 object detection...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    detect.run(weights=MODEL_PATH, source=IMAGE_DIR, save_txt=True, save_conf=True, project=OUTPUT_DIR)
    logging.info("Object detection completed.")

# Step 2: Process Detection Results
def process_results(output_folder):
    logging.info("Processing YOLOv5 detection results...")
    results = []
    
    for txt_file in Path(output_folder).rglob("*.txt"):
        with open(txt_file, "r") as f:
            for line in f:
                parts = line.strip().split()
                class_id, x, y, w, h, confidence = parts[0], *map(float, parts[1:])
                results.append([txt_file.stem, class_id, x, y, w, h, confidence])

    df = pd.DataFrame(results, columns=["Image", "ClassID", "X", "Y", "Width", "Height", "Confidence"])
    df.to_csv(RESULT_CSV, index=False)
    logging.info(f"Detection results saved to {RESULT_CSV}.")
    return df

# Step 3: Store Results in a Database
def store_results_in_db(csv_file):
    logging.info("Storing results in SQLite database...")
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_csv(csv_file)
    df.to_sql("yolo_detections", conn, if_exists="replace", index=False)
    conn.close()
    logging.info("Results stored in database.")

# Step 4: Run Everything
if __name__ == "__main__":
    try:
        run_object_detection()
        df = process_results(OUTPUT_DIR)
        store_results_in_db(RESULT_CSV)
        logging.info("Pipeline completed successfully.")
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
