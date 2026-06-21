import string
import random
import hashlib
import urllib.request


def generar_contrasena(longitud):
    minusculas = string.ascii_lowercase
    mayusculas = string.ascii_uppercase
    numeros = string.digits
    simbolos = string.punctuation

    contrasena = [
        random.choice(minusculas),
        random.choice(mayusculas),
        random.choice(numeros),
        random.choice(simbolos),
    ]
    todos = minusculas + mayusculas + numeros + simbolos
    contrasena += random.choices(todos, k=longitud - 4)
    random.shuffle(contrasena)
    return "".join(contrasena)


def verificar_filtracion(contrasena):
    sha1 = hashlib.sha1(contrasena.encode("utf-8")).hexdigest().upper()
    prefijo, sufijo = sha1[:5], sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefijo}"
    try:
        with urllib.request.urlopen(url, timeout=5) as respuesta:
            datos = respuesta.read().decode("utf-8")
    except Exception as e:
        print(f"No se pudo conectar a la API ({e}). Verifica tu conexión a internet.")
        return

    for linea in datos.splitlines():
        sufijo_api, veces = linea.split(":")
        if sufijo_api == sufijo:
            print(f"⚠️  Esta contraseña apareció en {veces} filtraciones conocidas. ¡Evítala!")
            return

    print("✅ Esta contraseña no aparece en filtraciones conocidas.")


longitud = int(input("Ingrese el tamaño de la contraseña: "))

if longitud < 4:
    print("La longitud mínima debe ser 4 para garantizar variedad.")
else:
    contrasena = generar_contrasena(longitud)
    print("La contraseña generada es:", contrasena)
    verificar_filtracion(contrasena)
    