import os

# DICCIONARIO: cada color tiene su etiqueta y su código de consola
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
    "MORADO": "\033[95m",  # colores agregados
    "CAFE": "\033[33m",
}

# TUPLA: respuestas afirmativas aceptadas.
# Es fija, por eso no es lista.
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def limpiar_pantalla():
    os.system("clear" if os.name == "posix" else "cls")


def imprimir_color(texto, color):
    # .get() evita un error si el color no existe.
    # Si no existe, utiliza BLANCO.
    codigo = COLORES.get(color, COLORES["BLANCO"])
    print(f"{codigo}{texto}{COLORES['RESET']}")


def imprimir_titulo(texto):
    limpiar_pantalla()
    imprimir_color("=" * 60, "AZUL")
    print(f"  {texto}".center(60))
    imprimir_color("=" * 60, "AZUL")
    print()


def imprimir_exito(mensaje):
    imprimir_color(f"✓ {mensaje}", "VERDE")


def imprimir_error(mensaje):
    imprimir_color(f"✗ {mensaje}", "ROJO")


def imprimir_info(mensaje):
    imprimir_color(f"ℹ {mensaje}", "CYAN")


def confirmar(pregunta):
    # Devuelve True si el usuario respondió algo de la
    # tupla RESPUESTAS_SI.
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    # Validación mínima: un @, algo antes del @,
    # un punto dentro del dominio y que el dominio
    # no termine en punto.
    texto = texto.strip()

    if texto.count("@") != 1:
        return False

    usuario, dominio = texto.split("@")

    return (
        len(usuario) > 0
        and "." in dominio
        and not dominio.endswith(".")
    )