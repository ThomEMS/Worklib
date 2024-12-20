import cv2
import numpy as np
import matplotlib.pyplot as plt

# Charger les images
image_baseline = cv2.imread("baseline.jpg")
image_20 = cv2.imread("luminaire_20.jpg")
image_50 = cv2.imread("luminaire_50.jpg")
image_100 = cv2.imread("luminaire_100.jpg")

images = [image_baseline, image_20, image_50, image_100]
labels = ["Baseline", "Luminaire 20%", "Luminaire 50%", "Luminaire 100%"]