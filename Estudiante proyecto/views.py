from models import Estudiante, CAMPOS_Estudiante
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/Estudiante.json")

# TUPLAS de configuración: fijas, nadie las modifica en tiempo de ejecución
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")  # Agregado carnet como obligatorio
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "carnet")  # Agregado carnet como buscable


# ===================== AYUDAS INTERNAS =====================

def emails_registrados(excepto_id=None):
    """
    CONJUNTO con los emails ya usados.
    Sirve para detectar duplicados rápidamente.

    excepto_id:
    Permite excluir al estudiante que estamos actualizando,
    para que pueda conservar su propio email.
    """
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


# Función para obtener y agregar notas
def agregar_nota(id_estudiante, nota, materia):
    # Leemos todos los estudiantes desde el archivo JSON.
    registros = gestor.leer()

    # Buscamos al estudiante por su ID.
    for registro in registros:
        if registro.get("id") == id_estudiante:

            # "notas" es un DICCIONARIO.
            #
            # La estructura será:
            # {
            #     "Matematicas": [15, 18],
            #     "Ingles": [17]
            # }
            #
            # Si "notas" todavía no existe, creamos un diccionario vacío.
            notas = registro.setdefault("notas", {})

            # Si la materia todavía no existe en el diccionario,
            # creamos una lista vacía para guardar sus notas.
            notas.setdefault(materia, [])

            # Agregamos la nueva nota a la lista de esa materia.
            notas[materia].append(nota)

            # "materias" se guarda como LISTA en el JSON.
            materias = registro.setdefault("materias", [])

            # Evitamos registrar dos veces la misma materia.
            if materia not in materias:
                materias.append(materia)

            # Guardamos los cambios en el archivo JSON.
            if gestor.guardar(registros):
                return True, "Nota agregada correctamente"

            return False, "No se pudo guardar la información"

    # Si terminamos el for y no encontramos el ID.
    return False, f"No existe un estudiante con id {id_estudiante}"





def materias_disponibles():
    """
    Devuelve un CONJUNTO con todas las materias
    registradas en las notas de los estudiantes.
    """
    registros = gestor.leer()

    return {
        nota["materia"]
        for registro in registros
        if "notas" in registro
        for nota in registro["notas"]
    }


def estudiantes_en_comun(id_estudiante1, id_estudiante2):
    """
    Devuelve un CONJUNTO con las materias
    que tienen en común dos estudiantes.
    """
    registros = gestor.leer()

    notas1 = next(
        (
            registro["notas"]
            for registro in registros
            if registro["id"] == id_estudiante1
        ),
        []
    )

    notas2 = next(
        (
            registro["notas"]
            for registro in registros
            if registro["id"] == id_estudiante2
        ),
        []
    )

    # CONJUNTOS con las materias de cada estudiante.
    materias1 = {nota["materia"] for nota in notas1}
    materias2 = {nota["materia"] for nota in notas2}

    # INTERSECTION devuelve solamente las materias que están
    # presentes en los dos conjuntos.
    return materias1.intersection(materias2)


def obtener_notas(id_estudiante):
    """
    Devuelve una LISTA de diccionarios con las notas del estudiante.
    """
    registros = gestor.leer()

    for registro in registros:
        if registro["id"] == id_estudiante:
            return registro.get("notas", [])

    # Si no existe el estudiante, devuelve una LISTA vacía.
    return []


def carnetes_registrados(excepto_id=None):
    """
    CONJUNTO con los carnets ya utilizados.

    excepto_id:
    Permite excluir al estudiante que estamos actualizando,
    evitando que su propio carnet sea considerado duplicado.
    """
    return {
        registro["carnet"].lower()
        for registro in gestor.leer()
        if registro.get("carnet")
        and registro["id"] != excepto_id
    }


def siguiente_id():
    """
    Obtiene el siguiente ID disponible.

    Si existen estudiantes:
        máximo ID + 1

    Si no existen:
        comienza desde 1.
    """
    ids = [registro["id"] for registro in gestor.leer()]

    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_estudiante(datos):
    """
    datos: diccionario con las claves de CAMPOS_Estudiante.
    Devuelve una TUPLA: (éxito, mensaje).
    """
    try:

        # 1) NORMALIZACIÓN
        # Creamos un DICCIONARIO con todos los campos del modelo.
        # strip() elimina espacios sobrantes al inicio y al final.
        valores = {
            campo: str(datos.get(campo, "")).strip()
            for campo in CAMPOS_Estudiante
        }

        # 2) VALIDACIÓN DE CAMPOS OBLIGATORIOS
        # Recorremos la TUPLA CAMPOS_OBLIGATORIOS.
        faltantes = [
            campo
            for campo in CAMPOS_OBLIGATORIOS
            if not valores[campo]
        ]

        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # 3) VALIDACIÓN DEL FORMATO DEL EMAIL
        if not es_email_valido(valores["email"]):
            return False, (
                f"El email '{valores['email']}' "
                f"no tiene un formato válido"
            )

        # 4) VALIDACIÓN DE EMAIL DUPLICADO
        # Buscamos dentro del CONJUNTO de emails registrados.
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"

        # 5) VALIDACIÓN DE CARNET DUPLICADO
        # Buscamos dentro del CONJUNTO de carnets registrados.
        if valores["carnet"].lower() in carnetes_registrados():
            return False, "Ese carnet ya está registrado"

        # 6) CREACIÓN DEL OBJETO DEL MODELO
        #
        # IMPORTANTE:
        # No debemos escribir:
        #
        # Estudiante = Estudiante(...)
        #
        # porque estaríamos usando el mismo nombre para la clase
        # y para el objeto.
        #
        # La clase se llama Estudiante.
        # El objeto se llama estudiante.
        estudiante = Estudiante(siguiente_id(), **valores)

        # 7) OBTENEMOS LA LISTA ACTUAL DE REGISTROS.
        registros = gestor.leer()

        # Convertimos el objeto Estudiante en DICCIONARIO
        # y lo agregamos a la LISTA.
        registros.append(estudiante.a_diccionario())

        # 8) GUARDAMOS la LISTA en el archivo JSON.
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return (
            True,
            f"Estudiante {estudiante.obtener_nombre_completo()} "
            f"creado con id {estudiante.id}"
        )

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    """
    Devuelve una LISTA de objetos Estudiante.
    """
    return [
        Estudiante.desde_diccionario(registro)
        for registro in gestor.leer()
    ]


def obtener_por_id(id_estudiante):
    """
    Busca un estudiante por su ID.
    Si lo encuentra, devuelve el objeto Estudiante.
    Si no lo encuentra, devuelve None.
    """
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante

    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(termino):
    """
    Búsqueda lineal:
    revisa registro por registro los campos
    definidos en CAMPOS_BUSCABLES.
    """
    termino = termino.strip().lower()

    # Si el término está vacío, no hacemos búsqueda.
    if not termino:
        return []

    encontrados = []

    # Recorremos cada registro.
    for registro in gestor.leer():

        # Recorremos la TUPLA de campos buscables.
        for campo in CAMPOS_BUSCABLES:

            # Convertimos el valor a texto y lo pasamos a minúsculas.
            if termino in str(
                registro.get(campo, "")
            ).lower():

                # Si encontramos coincidencia,
                # convertimos el DICCIONARIO en objeto Estudiante.
                encontrados.append(
                    Estudiante.desde_diccionario(registro)
                )

                # Ya encontramos coincidencia en este estudiante.
                # Pasamos al siguiente registro.
                break

    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    """
    cambios:
    DICCIONARIO que contiene únicamente
    los campos que se quieren modificar.
    """
    try:

        # 1) DIFERENCIA DE CONJUNTOS
        #
        # Detectamos si enviaron algún campo
        # que no existe en CAMPOS_Estudiante.
        desconocidos = set(cambios) - set(CAMPOS_Estudiante)

        if desconocidos:
            return False, (
                f"Campos no válidos: "
                f"{', '.join(sorted(desconocidos))}"
            )

        # No se puede actualizar si no enviaron cambios.
        if not cambios:
            return False, "No se indicó ningún cambio"

        # 2) VALIDACIÓN DEL EMAIL
        if "email" in cambios:

            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"

            # Excluimos al estudiante actual.
            # De esta manera puede conservar su propio email.
            if cambios["email"].lower() in emails_registrados(
                excepto_id=id_estudiante
            ):
                return False, "Ese email ya lo usa otro estudiante"

        # 3) VALIDACIÓN DEL CARNET
        if "carnet" in cambios:

            # También excluimos al estudiante actual.
            # Así puede conservar su propio carnet.
            if cambios["carnet"].lower() in carnetes_registrados(
                excepto_id=id_estudiante
            ):
                return False, "Ese carnet ya lo usa otro estudiante"

        # 4) LEEMOS TODOS LOS REGISTROS.
        registros = gestor.leer()

        posicion = None

        # enumerate() nos proporciona:
        # indice → posición dentro de la LISTA
        # registro → DICCIONARIO del estudiante
        for indice, registro in enumerate(registros):

            if registro["id"] == id_estudiante:
                posicion = indice
                break

        # Si no encontramos el ID, terminamos.
        if posicion is None:
            return False, (
                f"No existe un estudiante con id {id_estudiante}"
            )

        # 5) ACTUALIZAMOS EL DICCIONARIO
        # update() agrega o reemplaza los campos enviados.
        registros[posicion].update(cambios)

        # 6) GUARDAMOS los cambios.
        if not gestor.guardar(registros):
            return False, "No se pudo guardar la actualización"

        return (
            True,
            f"Estudiante {id_estudiante} "
            f"actualizado ({len(cambios)} campo/s)"
        )

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):

    registros = gestor.leer()

    # Construimos una LISTA nueva sin el estudiante
    # cuyo ID queremos eliminar.
    #
    # Es mejor que borrar directamente mientras
    # recorremos la lista.
    quedan = [
        registro
        for registro in registros
        if registro["id"] != id_estudiante
    ]

    # Si las dos listas tienen el mismo tamaño,
    # significa que no se encontró el ID.
    if len(quedan) == len(registros):
        return False, (
            f"No existe un estudiante con id {id_estudiante}"
        )

    # Guardamos la LISTA nueva.
    if not gestor.guardar(quedan):
        return False, "No se pudo guardar la eliminación"

    return True, f"Estudiante {id_estudiante} eliminado"


# ===================== EXTRA: estadísticas con conjuntos =====================

def estadisticas():
    """
    Devuelve un DICCIONARIO de resumen.
    Práctica de LISTAS, CONJUNTOS y DICCIONARIOS.
    """
    registros = gestor.leer()

    # CONJUNTO de ciudades sin repetir.
    ciudades = {
        r.get("ciudad", "").title()
        for r in registros
        if r.get("ciudad")
    }

    # CONJUNTO de dominios de correo sin repetir.
    dominios = {
        r["email"].split("@")[1].lower()
        for r in registros
        if "@" in r["email"]
    }

    # LISTA con los nombres de estudiantes
    # que no tienen teléfono.
    sin_telefono = [
        r["nombre"]
        for r in registros
        if not r.get("telefono")
    ]

    # DICCIONARIO con las estadísticas.
    return {
        "total": len(registros),
        "ciudades": sorted(ciudades),
        "dominios": sorted(dominios),
        "sin_telefono": sin_telefono,
    }