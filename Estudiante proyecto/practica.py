#Ejercicio 1 · Quitar duplicados conservando el orden
#Dada ciudades = ["Quito","Guayaquil","Quito","Cuenca","Guayaquil"], obtén una lista sin repetidos respetando el orden de aparición (un set solo no alcanza).
ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

vistas = set()      # conjunto de control: para preguntar rápido si ya apareció
unicas = []         # lista de resultado: conserva el orden
for ciudad in ciudades:
    if ciudad not in vistas:
        vistas.add(ciudad)
        unicas.append(ciudad)

print(unicas)   # ['Quito', 'Guayaquil', 'Cuenca']

#Ejercicio 2 · Contar con un diccionario
#Con la misma lista, arma un diccionario {"Quito": 2, "Guayaquil": 2, "Cuenca": 1}.
contadores = {}
for ciudad in ciudades:
    contadores[ciudad] = contadores.get(ciudad, 0) + 1

print(contadores)  # {'Quito': 2, 'Guayaquil': 2, 'Cuenca': 1}

#Ejercicio 3 · Conjuntos en acción
#inscritos_matematica = {"Ana","Luis","Sol","Marco"} y inscritos_ingles = {"Luis","Marco","Ruth"}. Responde con código: ¿quiénes están en las dos?, ¿quiénes solo en matemática?, ¿cuántos estudiantes distintos hay en total?
inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
inscritos_ingles = {"Luis", "Marco", "Ruth"}

# Quiénes están en las dos
en_ambos = inscritos_matematica & inscritos_ingles

# Quiénes solo están en matemática
solo_matematica = inscritos_matematica - inscritos_ingles

# Cuántos estudiantes distintos hay en total
estudiantes_distintos = len(inscritos_matematica | inscritos_ingles)

print("Quiénes están en las dos:", en_ambos)
print("Quiénes solo están en matemática:", solo_matematica)
print("Cuántos estudiantes distintos hay en total:", estudiantes_distintos)

#Ejercicio 4 · De lista de diccionarios a índice
#Con clientes = [{"id":1,"nombre":"Ana"},{"id":2,"nombre":"Luis"}], crea un diccionario {id: cliente} para acceder por id sin recorrer la lista. Luego imprime el nombre del id 2.
clientes = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]
indice_clientes = {cliente["id"]: cliente for cliente in clientes}
print(indice_clientes[2]["nombre"])  # Luis

#Ejercicio 5 · Tuplas como registros inmutables
#Dada ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)], imprime el mes con mayor venta y el total, usando desempaquetado de tuplas.
ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)]
mes_mayor_venta = max(ventas, key=lambda x: x[1])
total_ventas = sum(venta[1] for venta in ventas)

print("Mes con mayor venta:", mes_mayor_venta[0])
print("Total de ventas:", total_ventas)

#Ejercicio 6 · Sobre el proyecto
#Agrega al Controlador la función clientes_por_ciudad() que devuelva un diccionario {"Guayaquil": ["Ana", "Luis"], "Quito": ["Sol"]}.
class Controlador:
    def __init__(self):
        self.clientes = []  # Lista de diccionarios con información de clientes

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def clientes_por_ciudad(self):
        resultado = {}
        for cliente in self.clientes:
            ciudad = cliente.get("ciudad")
            nombre = cliente.get("nombre")
            if ciudad and nombre:
                if ciudad not in resultado:
                    resultado[ciudad] = []
                resultado[ciudad].append(nombre)
        return resultado

