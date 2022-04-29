from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pathlib import *
from selenium import webdriver
from random import randint
from time import sleep
import csv
import inspect
import os
import re

# Genera una instancia del navegador automatizado
def generarDriver():
    # print("Generando el driver (1)")
    rutaDriver = os.path.join(os.getcwd(), "chromedriver")
    driver = webdriver.Chrome(rutaDriver, chrome_options=Options())
    Options().add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/59.0.3071.115 Safari/537.36")
    return driver

# Loguea al profesional dentro del SISFE
def loguearProfesional(driver):
    # print("Función loguear profesional (2)")
    infoLogueo = leerInformacionLogin()
    ingresarAurl(driver)
    cargarDatosLogin(driver, infoLogueo)
    input("Complete el captcha y presione una tecla para continuar")
    navegar(driver)

# Lee la información necesaria para loguearse de un archivo csv
def leerInformacionLogin():
    # print("Leyendo la información del abogado para el login (2a)")
    informacion = open("datos.csv", "r", encoding="latin1")

    linea = informacion.readline()

    datosIngreso = linea.split(',')
    circunscripcion = datosIngreso[0]
    colegio = datosIngreso[1]
    matricula = datosIngreso[2]
    contraseña = datosIngreso[3]

    return [circunscripcion, colegio, matricula, contraseña]

# Ingresa a la página del login
def ingresarAurl(driver):
    # print("Entrando en la página para loguearse (2b)")
    driver.get('https://sisfe.justiciasantafe.gov.ar/login-matriculado')

# Carga la información en los elementos HTML del login
def cargarDatosLogin(driver, infoLogueo):
    # print("Cargando datos del abogado en login (2c)")
    droplistCircunscripcion = encontrarElemento(driver, "circunscripcion")
    droplistCircunscripcion.send_keys(infoLogueo[0])
    droplistColegio = encontrarElemento(driver, "colegio")
    droplistColegio.send_keys(infoLogueo[1])
    textfieldMatricula = encontrarElemento(driver, "matricula")
    textfieldMatricula.send_keys(infoLogueo[2])
    textfieldContraseña = encontrarElemento(driver, "contraseña")
    textfieldContraseña.send_keys(infoLogueo[3])

# Busca elementos e introduce esperas para reducir errores
def encontrarElemento(driver, nombreElemento):
    # print("Buscando elemento (2ci): ", nombreElemento)
    if (nombreElemento == "circunscripcion"):
        droplistCircunscripcion = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//select[@id="circunscripcion"]'))
        )
        return droplistCircunscripcion
    if (nombreElemento == "colegio"):
        droplistColegio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//select[@id="colegio"]'))
        )
        return droplistColegio
    if (nombreElemento == "matricula"):
        textfieldMatricula = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@id="matricula"]'))
        )
        return textfieldMatricula
    if (nombreElemento == "contraseña"):
        textfieldContraseña = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@id="password"]'))
        )
        return textfieldContraseña
    if (nombreElemento == "botonIngresar"):
        botonIngresar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@id="ingresar"]'))
        )
        return botonIngresar
    if (nombreElemento == "CUIJ"):
        textfieldCUIJ = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="cuij"]'))
        )
        return textfieldCUIJ
    if (nombreElemento == "efectuarBusqueda"):
        botonEfectuarBusqueda = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@id="efectuarBusqueda"]'))
        )
        return botonEfectuarBusqueda
    if (nombreElemento == "linkCUIJ"):
        linkCUIJ = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@href,"/detalle-expediente/")]'))
        )
        return linkCUIJ
    if (nombreElemento == "botonPasarPagina"):
        #botonPasarPagina = driver.wait.until(
        #    EC.element_to_be_clickable(
        #        (By.XPATH, '//app-paginacion//li[@class="page-item next-item enabled"]')))
        botonPasarPagina = WebDriverWait(driver,20).until(
            EC.presence_of_element_located(
                (By.XPATH,'//app-paginacion//li[@class="page-item next-item enabled"]')
            )
        )
        return botonPasarPagina
    if (nombreElemento == "botonDesplegar"):
        botonDesplegar = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//form[@class="ng-valid ng-dirty ng-touched"]//div[@class="card-header"]//i'))
        )
        return botonDesplegar
    if (nombreElemento == "fecha"):
        fecha = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//table//tbody//td[1]/span/span').text)
        )
        return fecha
    if (nombreElemento == "textoAdjunto"):
        textoAdjunto = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//table//tbody//td[2]/span/span'.text)
            )
        )
        return textoAdjunto
    if (nombreElemento == "archivoAdjunto"):
        archivoAdjunto = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//table//tbody//td[4]/span/button/i')
            )
        )
        print("SE ENCONTRÓ EL ADJUNTO")
        return archivoAdjunto
    

# Navega a través del sitio para llegar a la página deseada
def navegar(driver):
    llamador = inspect.stack()[1][3]
    print("LO LLAMA LA FUNCIÓN: ")
    print(llamador)

    if (llamador == "loguearProfesional"):
        botonIngresar = encontrarElemento(driver, "botonIngresar")
        botonIngresar.click()
    if (llamador == "leerInformacionExpediente"):
        sleep(2)
        resultado = extraerSegundoAdjunto(driver)
        return resultado 

# Extrae el segundo archivo (que está en otra página)
def extraerSegundoAdjunto(driver):
    print("Entrando en la función 'extraerSegundoAdjunto'")
    # fecha = driver.find_element_by_xpath("//table//tbody//td[1]/span/span").text
    fecha = encontrarElemento(driver, "fecha")
    print("FECHA: ", fecha)
    # textoAdjunto = driver.find_element_by_xpath("//table//tbody//td[2]/span/span").text
    textoAdjunto = encontrarElemento(driver,"textoAdjunto")
    print("TEXTO ADJUNTO: ", textoAdjunto)
    # archivoAdjunto = driver.find_element_by_xpath("//table//tbody//td[4]/span/button/i")
    # archivoAdjunto = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//table//tbody//td[4]/span/button")))
    # archivoAdjunto = driver.find_element_by_xpath("//table//tbody//td[4]/span/button/i")
    archivoAdjunto = encontrarElemento(driver, "archivoAdjunto")
    archivoAdjunto.click()
    print("SUPUESTAMENTE YA LE HIZO CLICK")
    sleep(2)
    paginaAnterior(driver)
    return [fecha, textoAdjunto]

def paginaAnterior(driver):
    driver.execute_script("window.history.go(-1)")
    # driver.back()

# Busca el expediente dentro del SISFE por CUIJ
def buscarExpediente(driver):
    #print("Función buscar expediente (4)")
    cuijs = leerCUIJ()
    cargarCUIJ(driver, cuijs)
    navegar(driver)

# Lee el archivo y agrupa los CUIJS a buscar
def leerCUIJ():
    cuijs = []
    # print("Leyendo los CUIJs (4a)")
    listaCUIJs = open("cuijs.csv", "r", encoding="latin1")
    for fila in listaCUIJs:
        print(fila)
        cuijs.append(fila)
    return cuijs

# Carga el CUIJ y efectúa la búsqueda
def cargarCUIJ(driver, cuijs):
    scrollArriba(driver)
    # print("Cargando CUIJ (4b)")
    # desplegarCuadroBusqueda(driver)
    textfieldCUIJ = encontrarElemento(driver, "CUIJ")
    # CUIJ con 39 registros (con paginación): 21-26361795-6. Adjuntos: 21 A1 - 19 A2
    # CUIJ con 10 registros (sin paginación): 21-26362099-9. Adjuntos: 5 A1 - 5 A2
    # CUIJ con 54 registros (con paginación): 21-05016495-8. Adjuntos: 36 A1 - 
    textfieldCUIJ.send_keys("21-26361795-6")
    botonEfectuarBusqueda = encontrarElemento(driver, "efectuarBusqueda")
    botonEfectuarBusqueda.click()
    linkCUIJ = encontrarElemento(driver, "linkCUIJ")
    linkCUIJ.click()
    extraerInformacion(driver)

def desplegarCuadroBusqueda(driver):
    try:
        botonDesplegarBusqueda = encontrarElemento(driver, "botonDesplegar")
        botonDesplegarBusqueda.click()
    except:
        paginaAnterior(driver)
        desplegarCuadroBusqueda(driver)

# Extrae y guarda la información recolectada
def extraerInformacion(driver):
    print("Función extraer información (5)")
    sleep(5)
    filas = driver.find_elements_by_xpath("//table/tbody/tr")
    numeroFilas = len(filas)
    leerInformacionExpediente(driver, numeroFilas)
    botonPasarPagina = encontrarElemento(driver, "botonPasarPagina")
    if (botonPasarPagina):
        pasarPagina(driver)

# Toma la información correspondiente a los movimientos del expediente
def leerInformacionExpediente(driver, numeroFilas):
    # print("Trayendo información (5a)")
    sleep(10)

    # xpathBase = "//div[@class='table-responsive mt-2']//tbody/tr[i]"

    for i in range(1,numeroFilas+1):
        print("Vuelta número: ", i)
        try:
            tipoMovimiento1 = encontrarElemento(driver, "tipoMovimiento1")
            tipoMovimiento1 = driver.find_element(
                # By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(numeroFilas)+"]//td[1]//i").get_attribute('class')
                By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]//td[1]//i").get_attribute('class')
            tipoMov1 = identificarMovimiento(tipoMovimiento1)
            print(tipoMov1)
        except:
            tipoMov1 = "vacío"
            print("Vacío")
        try:
            tipoMovimiento2 = driver.find_element(
                By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[2]//i").get_attribute('class')
            #tipoMovimientoModif = identificarMovimiento(tipoMovimiento2)
            tipoMov2 = identificarMovimiento(tipoMovimiento2)
            print(tipoMov2)
        except:
            tipoMov2 = "vacío"
        try:
            fecha = driver.find_element(
                By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[3]/span/span").text
            print(fecha)
        except:
            fecha = "vacío"
        try:
            novedad = driver.find_element(
                By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[4]/span/span").text
            print(novedad)
        except:
            novedad = "vacío"
        try:
            observacion = driver.find_element(
                By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[5]/span/span").text
            observacion = observacion.replace("\n", " // ")
            print(observacion)
        except:
            observacion = "vacío"
        try:
            scrollSuave(driver)
            scrollSuave(driver)
            adjunto1 = driver.find_element(
                By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[6]//button/i")
            adjunto1.click()
            sleep(5)
        except:
            pass
        try:
            scrollSuave(driver)
            scrollSuave(driver)
            adjunto2 = driver.find_element(
                By.XPATH, "//div[@class='table-responsive mt-2']//tbody/tr["+str(i)+"]/td[8]//button/i")
            adjunto2.click()
            sleep(5)
            
            textoYfechaAdjunto = navegar(driver)
        except:
            pass
        guardarInformacion(tipoMov1, tipoMov2, fecha, novedad, observacion)

# Evalúa la necesidad (o no) de pasar página
def pasarPagina(driver):
    # print("Pasando página (5b)")
    try:
        scroll(driver)
        scrollSuave(driver)
        scroll(driver)
        scrollSuave(driver)
        botonPasarPagina = encontrarElemento(driver, "botonPasarPagina")
        botonPasarPagina.click()
        print("Fin del try - pasa página y vuelve a traer información")
        sleep(5)
    except:
        print("NO se ha encontrado otra página.")
        pass

# Utiliza la lista de referencias para interpretar el ícono encontrado
def identificarMovimiento(movimiento):
    # print("Identificando movimiento. Clase: ",movimiento)
    result1 = movimiento.find("file")
    result2 = movimiento.find("gavel")
    result3 = movimiento.find("shield")
    result4 = movimiento.find("user-check")

    encontrado = 15

    if (result1 == encontrado):
        mov = "Escrito"
    if (result2 == encontrado):
        mov = "Resolución/Sentencia"
    if (result3 == encontrado):
        mov = "Trámite"
    if (result4 == encontrado):
        mov = "Notificaciones con firma digital"
    return mov

# Guarda la información recolectada
def guardarInformacion(tipoMov1, tipoMov2, fecha, novedad, observacion):
    # print("Guardando información (5c)")
    with open('datosExtraidos.csv', 'a', newline='') as f:
        writer = csv.writer(f, delimiter = ',', lineterminator='\n')
        writer.writerow([tipoMov1, tipoMov2, fecha, novedad, observacion])

def scroll(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

def scrollSuave(driver):
    driver.execute_script("window.scrollTo(0, window.scrollY + 300)")

def scrollArriba(driver):
    driver.execute_script("window.scrollBy(0,0)","")
    
# def scrollIntoView:
#     element.scrollIntoView({block: "end"});
