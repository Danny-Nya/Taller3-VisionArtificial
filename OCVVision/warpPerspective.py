import cv2, glob, os
import numpy as np
from PIL import Image


def main():
    # Transformacion en perspectiva
    imagen = cv2.imread("imagesWarpPerspective/input.jpg")
    # los puntos en donde estan los puntos que se quieren transformar
    pts1 = np.float32([[157, 41], [405, 87], [187, 299], [401, 250]])
    # los puntos a donde se quiere llevar la imagen de resultado
    pts2 = np.float32([[0, 0], [686, 0], [0, 386], [686, 386]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(imagen, M, (686, 386))
    cv2.imwrite("resultsWarpPerspective/result.png", dst)
    # https://medium.com/analytics-vidhya/opencv-perspective-transformation-9edffefb2143

if __name__ == '__main__':
    main()
