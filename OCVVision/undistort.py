import cv2, glob, os
import numpy as np
from PIL import Image

#-------------------------------------------------------------------------------------------------
# ARREGO DE DISTORCIÓN DE CAMARA CALIBRACIÓN
# Tamaño del tablero de ajedrez (número de esquinas internas)
num_corners_x = 7
num_corners_y = 6

# Lista para almacenar puntos de objeto (3D) y puntos de imagen (2D) de todas las imágenes.
objpoints = []  # Puntos de objeto en 3D
imgpoints = []  # Puntos de imagen en 2D

# Ruta a las imágenes de calibración
imagenes = glob.glob("imagesUndistort/*.jpg")

# Utilizar solo los primeros dos imágenes para la depuración
debug_images = imagenes[:2]

# Preparar puntos de objeto en el mundo real
objp = np.zeros((num_corners_x * num_corners_y, 3), np.float32)
objp[:, :2] = np.mgrid[0:num_corners_x, 0:num_corners_y].T.reshape(-1, 2)

# Variables para el procesamiento de las imágenes
gray = None  # Definir gray fuera del loop

# Procesamiento de imágenes para calibración
for fname in imagenes:
    img = cv2.imread(fname)
    if img is None:
        print(f"Error reading image: {fname}")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (num_corners_x, num_corners_y), None)
    if not ret:
        print(f"Chessboard corners not found in image: {fname}")
        continue

    objpoints.append(objp)
    imgpoints.append(corners)

# Calibrar la cámara y obtener los parámetros de corrección de distorsión
if len(objpoints) > 0 and len(imgpoints) > 0:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
else:
    print("No valid calibration data.")

# Corregir distorsión y guardar las imágenes corregidas
output_directory = "./resultsUndistort/"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for fname in imagenes:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    undistorted_img = cv2.undistort(gray, mtx, dist, None, newcameramtx)

    output_filename = 'undistorted_' + os.path.basename(fname)

    try:
        pil_img = Image.fromarray(undistorted_img)
        pil_img.save(os.path.join(output_directory, output_filename))
        print(f"Saved: {output_filename}")
    except Exception as e:
        print(f"Error saving {output_filename}: {e}")