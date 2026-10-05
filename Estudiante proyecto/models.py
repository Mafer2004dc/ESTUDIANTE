import json

# TUPLA de campos: el orden y los nombres son fijos, por eso no es una lista.
# La usan el Controlador y la Vista para no repetir textos sueltos.
CAMPOS_Estudiante = ("nombre", "apellido", "email", "carnet")


class Estudiante:
    """MODELO: representa a un estudiante."""

    def __init__(self, id_estudiante, nombre, apellido, email, carnet,
                 notas=None, materias=None):

        # Identificador único del estudiante
        self.id = id_estudiante

        # Datos básicos del estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet

        # DICCIONARIO DE LISTAS:
        # Ejemplo:
        # {
        #     "Matemática": [18, 19],
        #     "Inglés": [17]
        # }
        self.notas = notas if notas else {}

        # CONJUNTO:
        # Guarda las materias inscritas sin permitir repetidas.
        # Ejemplo:
        # {"Matemática", "Inglés"}
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self):
        # Une el nombre y el apellido del estudiante.
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        # add() agrega la materia al conjunto.
        # Si ya existe, no se duplica.
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        # Primero aseguramos que el estudiante esté inscrito
        # en esa materia.
        self.inscribir_materia(materia)

        # setdefault() crea una lista vacía si la materia
        # todavía no existe en el diccionario.
        #
        # Después append() agrega la nota a esa lista.
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self):
        # Lista donde reuniremos todas las notas.
        todas = []

        # Recorremos las listas de notas de cada materia.
        for lista_notas in self.notas.values():
            todas.extend(lista_notas)

        # Si el estudiante todavía no tiene notas,
        # devolvemos 0.
        if not todas:
            return 0

        # Calculamos el promedio.
        return round(sum(todas) / len(todas), 2)

    def materias_en_comun(self, otro_estudiante):
        # INTERSECCIÓN de conjuntos.
        # Devuelve las materias que tienen ambos estudiantes.
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        # Convierte el objeto Estudiante en un diccionario.
        # Esto permite posteriormente guardarlo en JSON.
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,

            # El diccionario de notas se puede guardar directamente
            # en JSON.
            "notas": self.notas,

            # JSON no maneja directamente los conjuntos (set),
            # por eso lo convertimos temporalmente en una lista.
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        # Convierte un diccionario nuevamente en un objeto Estudiante.
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],

            # Recuperamos las notas.
            notas=datos.get("notas", {}),

            # Recuperamos las materias y las convertimos
            # nuevamente en un conjunto.
            materias=set(datos.get("materias", [])),
        )

    def a_json(self):
        # Convierte el diccionario del estudiante en texto JSON.
        return json.dumps(
            self.a_diccionario(),
            ensure_ascii=False
        )

    def __str__(self):
        # Define cómo se mostrará el estudiante cuando
        # utilicemos print() sobre un objeto Estudiante.
        return f"[{self.id}] {self.obtener_nombre_completo()} - {self.email}"