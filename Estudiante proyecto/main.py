from models import CAMPOS_Estudiante, Estudiante
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, estadisticas,
    agregar_nota, estudiantes_en_comun
)


def pausa():
    # Detiene el programa hasta que el usuario presione Enter.
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    # Muestra los encabezados de la tabla.
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CARNET':<15}{'PROMEDIO':<10}")

    print("-" * 85)

    # Recorremos la LISTA de estudiantes.
    for estudiante in estudiantes:
        print(
            f"{estudiante.id:<5}"
            f"{estudiante.obtener_nombre_completo():<25}"
            f"{estudiante.email:<28}"
            f"{estudiante.carnet:<15}"
            f"{estudiante.obtener_promedio():<10}"
        )

    print("-" * 85)

    # len() indica cuántos estudiantes tiene la LISTA.
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


# ---------- C · CREAR ----------

def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")

    # Recorro la TUPLA de campos.
    # Si se agrega un campo al Modelo y a CAMPOS_Estudiante,
    # este formulario podrá utilizarlo automáticamente.
    datos = {}

    for campo in CAMPOS_Estudiante:
        datos[campo] = input(f"{campo.capitalize()}: ")

    # crear_estudiante() devuelve una TUPLA:
    # (True/False, mensaje)
    exito, mensaje = crear_estudiante(datos)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# ---------- R · LEER TODOS ----------

def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")

    # Obtenemos una LISTA de objetos Estudiante.
    estudiantes = obtener_todos()

    if not estudiantes:
        imprimir_info(
            "Todavía no hay estudiantes. "
            "Use la opción 1 para crear el primero."
        )
    else:
        mostrar_tabla(estudiantes)

    pausa()


# ---------- S · BUSCAR ----------

def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTES")

    termino = input("Nombre, email, teléfono o ciudad: ")

    # buscar_estudiantes() devuelve una LISTA
    # con los estudiantes encontrados.
    encontrados = buscar_estudiantes(termino)

    if not encontrados:
        imprimir_info(
            f"Ningún estudiante coincide con '{termino}'."
        )
    else:
        mostrar_tabla(encontrados)

    pausa()


# ---------- R · LEER UNO ----------

def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")

    try:
        # Convertimos la entrada de texto a ENTERO.
        id_estudiante = int(input("Id del estudiante: "))

    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    # Buscamos el estudiante mediante su ID.
    estudiante = obtener_por_id(id_estudiante)

    if not estudiante:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )

    else:
        # Convertimos el objeto a DICCIONARIO.
        # items() permite recorrer clave y valor al mismo tiempo.
        for clave, valor in estudiante.a_diccionario().items():
            print(
                f"  {clave.capitalize():<12}: {valor}"
            )

    pausa()


# ---------- U · ACTUALIZAR ----------

def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")

    try:
        # El ID debe ser un número entero.
        id_estudiante = int(input("Id del estudiante: "))

    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    # Buscamos primero el estudiante.
    estudiante = obtener_por_id(id_estudiante)

    if not estudiante:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
        return pausa()

    # Mostramos el nombre del estudiante que se editará.
    imprimir_info(
        f"Editando a {estudiante.obtener_nombre_completo()}"
    )

    print(
        "Deje en blanco el campo que no quiera cambiar.\n"
    )

    # DICCIONARIO donde solamente guardaremos
    # los campos que el usuario quiera modificar.
    cambios = {}

    # Recorremos la TUPLA de campos del modelo.
    for campo in CAMPOS_Estudiante:

        # getattr() obtiene dinámicamente el valor
        # del atributo del objeto.
        actual = getattr(estudiante, campo)

        nuevo = input(
            f"{campo.capitalize()} [{actual}]: "
        ).strip()

        # Si el usuario escribió algo,
        # agregamos ese campo al DICCIONARIO.
        if nuevo:
            cambios[campo] = nuevo

    # Enviamos solamente los cambios al controlador.
    exito, mensaje = actualizar_estudiante(
        id_estudiante,
        cambios
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# ---------- D · ELIMINAR ----------

def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")

    try:
        id_estudiante = int(input("Id del estudiante: "))

    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    # Primero comprobamos que exista.
    estudiante = obtener_por_id(id_estudiante)

    if not estudiante:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
        return pausa()

    # Mostramos quién será eliminado.
    imprimir_info(
        f"Se eliminará: "
        f"{estudiante.obtener_nombre_completo()} "
        f"(id {estudiante.id})"
    )

    # confirmar() devuelve True o False.
    if confirmar("¿Confirma la eliminación?"):

        exito, mensaje = eliminar_estudiante(
            id_estudiante
        )

        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)

    else:
        imprimir_info("Operación cancelada")

    pausa()


# ---------- EXTRA · ESTADÍSTICAS ----------

def opcion_estadisticas():
    imprimir_titulo("ESTADÍSTICAS")

    # Recibimos un DICCIONARIO de estadísticas.
    datos = estadisticas()

    print(
        f"  Estudiantes registrados : "
        f"{datos['total']}"
    )

    print(
        f"  Ciudades distintas      : "
        f"{len(datos['ciudades'])} -> "
        f"{', '.join(datos['ciudades'])}"
    )

    print(
        f"  Dominios de email       : "
        f"{', '.join(datos['dominios'])}"
    )

    print(
        f"  Sin teléfono             : "
        f"{len(datos['sin_telefono'])}"
    )

    pausa()


def salir():
    # Esta función devuelve "salir" para que main()
    # sepa que debe terminar el programa.
    imprimir_info("¡Hasta luego! 👋")
    return "salir"


# ----------- EXTRA · VER PROMEDIO DE ESTUDIANTES -----------

def opcion_ver_promedio():
    imprimir_titulo("PROMEDIO DE ESTUDIANTES")

    # Obtenemos todos los estudiantes.
    # La tabla utiliza el atributo promedio del modelo.
    estudiantes = obtener_todos()

    if not estudiantes:
        imprimir_info(
            "Todavía no hay estudiantes. "
            "Use la opción 1 para crear el primero."
        )
    else:
        mostrar_tabla(estudiantes)

    pausa()


# ----------- EXTRA · AGREGAR NOTA -----------

def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA A ESTUDIANTE")

    try:
        id_estudiante = int(
            input("Id del estudiante: ")
        )

    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    # Comprobamos que el estudiante exista.
    estudiante = obtener_por_id(id_estudiante)

    if not estudiante:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
        return pausa()

    # Pedimos la materia.
    materia = input("Materia: ").strip()

    # Verificamos que no esté vacía.
    if not materia:
        imprimir_error("La materia no puede estar vacía")
        return pausa()

    try:
        # Convertimos la nota a FLOAT para permitir
        # valores como 18.5.
        nota = float(input("Nota: "))

    except ValueError:
        imprimir_error("La nota debe ser un número")
        return pausa()

    # Utilizamos la función agregar_nota() del views.py.
    # Esta función se encarga de guardar la nota
    # dentro del registro correspondiente.
    exito, mensaje = agregar_nota(
        id_estudiante,
        nota,
        materia
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# ----------- EXTRA · MATERIAS EN COMÚN -----------

def materias_en_comun(id_estudiante1, id_estudiante2):
    imprimir_titulo(
        "MATERIAS EN COMÚN ENTRE DOS ESTUDIANTES"
    )

    # Buscamos ambos estudiantes.
    estudiante1 = obtener_por_id(id_estudiante1)
    estudiante2 = obtener_por_id(id_estudiante2)

    if not estudiante1 or not estudiante2:
        imprimir_error(
            "Uno o ambos estudiantes no existen."
        )
        return pausa()

    # Utilizamos la función del views.py.
    # Esta devuelve un CONJUNTO con las materias
    # que ambos estudiantes tienen en común.
    materias_comunes = estudiantes_en_comun(
        id_estudiante1,
        id_estudiante2
    )

    if materias_comunes:

        print(
            f"Materias en común entre "
            f"{estudiante1.obtener_nombre_completo()} "
            f"y "
            f"{estudiante2.obtener_nombre_completo()}:"
        )

        # sorted() ordena el CONJUNTO alfabéticamente
        # antes de mostrarlo.
        for materia in sorted(materias_comunes):
            print(f"  - {materia}")

    else:
        imprimir_info(
            "No hay materias en común entre "
            "los dos estudiantes."
        )

    pausa()


# DICCIONARIO de opciones:
# tecla -> (texto del menú, función)
#
# El DICCIONARIO permite relacionar cada opción
# del menú directamente con la función que debe ejecutar.
OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Estadísticas", opcion_estadisticas),
    "8": ("Ver promedio", opcion_ver_promedio),
    "9": ("Agregar nota", opcion_agregar_nota),

    "10": (
        "Materias en común",
        lambda: materias_en_comun(
            int(input("Id del primer estudiante: ")),
            int(input("Id del segundo estudiante: "))
        )
    ),

    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo(
        "SISTEMA DE GESTIÓN DE ESTUDIANTES"
    )

    # Recorremos el DICCIONARIO de opciones.
    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")

    print()


def main():

    # El menú se mantiene ejecutándose
    # hasta que el usuario seleccione salir.
    while True:

        mostrar_menu()

        tecla = input(
            "Seleccione una opción: "
        ).strip()

        # Búsqueda instantánea por clave
        # dentro del DICCIONARIO OPCIONES.
        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue

        # Obtenemos la función asociada a la opción.
        _texto, funcion = OPCIONES[tecla]

        # Ejecutamos la función.
        # Si devuelve "salir", terminamos el while.
        if funcion() == "salir":
            break


# Este bloque ejecuta main() solamente
# cuando ejecutamos directamente este archivo.
if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print(
            "\nPrograma interrumpido por el usuario."
        )