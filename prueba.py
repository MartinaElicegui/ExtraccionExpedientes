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

print("Leyendo la información del abogado para el login (2a)")
informacion = open("datos.csv", "r", encoding="latin1")

linea = informacion.readline()

datosIngreso = linea.split(',')
circunscripcion = datosIngreso[0]
colegio = datosIngreso[1]
matricula = datosIngreso[2]
contraseña = datosIngreso[3]

result = [circunscripcion, colegio, matricula, contraseña]
print("Es del tipo: ", type(circunscripcion))