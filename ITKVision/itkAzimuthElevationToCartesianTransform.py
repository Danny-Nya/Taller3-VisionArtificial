# Importa la biblioteca itk
import itk

def main():
    # Crea un punto en coordenadas esféricas (3D) utilizando el tipo de datos itk.Point
    spherical = itk.Point[itk.D, 3]()
    spherical[0] = 0.0         # Radio (distancia desde el origen)
    spherical[1] = 45.0        # Elevación en grados
    spherical[2] = 1.0         # Ángulo azimutal en radianes

    # Crea una instancia de la transformación AzimuthElevationToCartesianTransform
    azimuthElevation = itk.AzimuthElevationToCartesianTransform[itk.D, 3].New()

    # Aplica la transformación para convertir las coordenadas esféricas a cartesianas
    cartesian = azimuthElevation.TransformAzElToCartesian(spherical)

    # Imprime los valores de las coordenadas esféricas y cartesianas
    print("spherical:", spherical)
    print("Cartesian:", cartesian)


if __name__ == "__main__":
    main()