import sys
from funciones import *

def main():
    driver = generarDriver()
    driver.maximize_window()
    loguearProfesional(driver)
    buscarExpediente(driver)
    input("Presione una tecla para terminar")
    
if __name__ == "__main__":
    sys.exit(main())

