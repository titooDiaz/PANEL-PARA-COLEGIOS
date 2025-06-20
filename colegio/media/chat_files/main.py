import mpmath
import time
import sys
import os

# Configura precisión inicial
mpmath.mp.dps = 1000  # Precisión inicial
contador = 0
pi_str = str(mpmath.mp.pi)[2:]  # Decimales de pi como string
salida = "3."  # Comenzamos con la parte entera

try:
    while True:
        # Si ya no hay más dígitos, incrementa precisión
        if contador >= len(pi_str):
            mpmath.mp.dps += 1000
            pi_str = str(mpmath.mp.pi)[2:]

        salida += pi_str[contador]
        contador += 1
        
        os.system('cls' if os.name == 'nt' else 'clear')

        print(salida)
        print(f"\nDecimales mostrados: {contador}")

        time.sleep(0.00001) 
except KeyboardInterrupt:
    print("\nInterrupción del usuario.")
