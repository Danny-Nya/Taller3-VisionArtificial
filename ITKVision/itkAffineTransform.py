# Importa las bibliotecas necesarias
import SimpleITK as sitk
import numpy as np

# Define una función principal llamada 'main'
def main():
    # Define la dimensión de la transformación (2D en este caso)
    Dimension = 2

    # Crea una matriz de transformación de ceros y define los valores de rotación y traslación
    matrix = np.zeros((Dimension + 1, Dimension + 1), dtype=float)
    matrix[0, 0] = np.cos(0.50)  # Componente coseno de la rotación
    matrix[0, 1] = np.sin(0.50)  # Componente seno de la rotación
    matrix[0, 2] = 0.0           # Componente X de la traslación

    matrix[1, 0] = -matrix[0, 1]  # Componente inversa del seno para la inversa de la rotación
    matrix[1, 1] = matrix[0, 0]   # Componente coseno de la inversa de la rotación
    matrix[1, 2] = 0.0           # Componente Y de la traslación

    matrix[2, 0] = 0.0           # Componente constante para mantener inalterada la dimensión z
    matrix[2, 1] = 0.0           # Componente constante para mantener inalterada la dimensión z
    matrix[2, 2] = 1.0           # Componente constante para mantener inalterada la dimensión z

    # Lee una imagen de entrada utilizando SimpleITK
    input = sitk.ReadImage("ImageAffineTransform/input.png")

    # Obtiene el tipo de píxel y el tamaño de la imagen de entrada
    PixelType = input.GetPixelID()
    size = input.GetSize()

    # Crea un filtro de re-muestreo
    resample = sitk.ResampleImageFilter()
    resample.SetOutputPixelType(PixelType)
    resample.SetReferenceImage(input)
    resample.SetSize(size)

    # Configura el interpolador para el re-muestreo
    resample.SetInterpolator(sitk.sitkHammingWindowedSinc)

    # Define el tipo de transformación como una transformación afín
    TransformType = sitk.AffineTransform(Dimension)

    # Prepara los parámetros de la transformación afín
    parameters = [0] * (Dimension * Dimension + Dimension)
    for i in range(Dimension):
        for j in range(Dimension):
            parameters[i * Dimension + j] = matrix[i, j]
    for i in range(Dimension):
        parameters[i + Dimension * Dimension] = matrix[i, Dimension]
    TransformType.SetParameters(parameters)

    # Asigna la transformación al filtro de re-muestreo
    resample.SetTransform(TransformType)

    # Ejecuta el re-muestreo de la imagen de entrada
    fin = resample.Execute(input)

    # Guarda la imagen re-muestreada en un archivo de salida
    sitk.WriteImage(fin, "ResultAffineTransform/output.jpg")

if __name__ == "__main__":
    main()
