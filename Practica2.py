import random

def generar_entorno(tamano, num_sucias, num_obstaculos):
    # Crear entorno con todas las celdas limpias inicialmente
    entorno = ["limpia"] * tamano
    
    if num_sucias + num_obstaculos > tamano:
        num_sucias = tamano - num_obstaculos  # Limitar el número de celdas sucias

    # Colocar obstáculos
    indices_obstaculos = random.sample(range(tamano), num_obstaculos)
    for i in indices_obstaculos:
        entorno[i] = "obstáculo"

    # Colocar celdas sucias y muy sucias
    indices_sucias = random.sample([i for i in range(tamano) if entorno[i] != "obstáculo"], num_sucias)
    for i in indices_sucias:
        if random.random() < 0.5:  # 50% probabilidad de que sea muy sucia
            entorno[i] = "muy sucia"
        else:
            entorno[i] = "sucia"
    
    return entorno

def mostrar_entorno(entorno, posicion):
    print("Entorno:", " ".join([f"[{entorno[i][0]}]" if i != posicion else "[X]" for i in range(len(entorno))]))

class AspiradoraInteligente:
    def __init__(self, entorno, posicion_inicial):
        self.entorno = entorno
        self.posicion = posicion_inicial
        self.bateria = 20  # Limite de batería por carga
        self.acciones = 0
        self.posicion_inicial = posicion_inicial
        self.movimientos = 0
        self.limpiezas = 0
        self.celdas_limpiadas = 0

    def limpiar(self):
        """Realiza la limpieza en la celda actual."""
        if self.entorno[self.posicion] == "sucia":
            self.entorno[self.posicion] = "limpia"
            self.limpiezas += 1
            self.celdas_limpiadas += 1
            self.acciones += 1
            print(f"Limpieza realizada en la posición {self.posicion}.")
        elif self.entorno[self.posicion] == "muy sucia":
            self.entorno[self.posicion] = "limpia"
            self.limpiezas += 2
            self.celdas_limpiadas += 1
            self.acciones += 2
            print(f"Limpieza profunda realizada en la posición {self.posicion}.")

    def mover(self, direccion):
        """Se mueve a la izquierda o derecha si no hay obstáculos y si hay batería."""
        if self.bateria > 0:
            nueva_posicion = self.posicion + direccion
            # Evitar mover fuera de los límites o sobre un obstáculo
            if 0 <= nueva_posicion < len(self.entorno) and self.entorno[nueva_posicion] != "obstáculo" and nueva_posicion != self.posicion_inicial:
                self.posicion = nueva_posicion
                self.movimientos += 1
                self.bateria -= 1
                self.acciones += 1
                print(f"Moviendo a la posición {self.posicion}.")
            else:
                print("Movimiento bloqueado por obstáculo o borde.")
        else:
            print("Batería agotada.")

    def cargar(self):
        """Regresa a la posición inicial para recargar sin consumir batería."""
        print("Batería agotada. Regresando a la posición inicial para recargar...")
        # Evitar que la posición inicial sea tratada como un obstáculo
        while self.posicion != self.posicion_inicial:
            # Mover sin gastar batería
            self.posicion += -1 if self.posicion > self.posicion_inicial else 1
            self.acciones += 1
            print(f"Moviendo a la posición {self.posicion} para recargar.")
        # Recargar batería
        self.bateria = 20
        self.acciones += 1
        print("Batería recargada.")

    def ejecutar(self):
        """Ejecuta el proceso de limpieza hasta que todas las celdas alcanzables estén limpias."""
        while True:
            if self.bateria == 0:
                self.cargar()  # Recargar si la batería se ha agotado

            # Mostrar el entorno
            mostrar_entorno(self.entorno, self.posicion)
            
            # Limpiar si la celda está sucia o muy sucia
            self.limpiar()
            
            # Verificar si todas las celdas alcanzables están limpias
            if all(celda == "limpia" or celda == "obstáculo" for celda in self.entorno):
                print("¡Todas las celdas alcanzables están limpias! Tarea completada.")
                break
            
            # Intentar mover en cualquier dirección (izquierda o derecha), con los nuevos límites
            if self.posicion > 0 and self.entorno[self.posicion - 1] != "obstáculo" and self.posicion - 1 != self.posicion_inicial:
                self.mover(-1)  # Mover a la izquierda
            elif self.posicion < len(self.entorno) - 1 and self.entorno[self.posicion + 1] != "obstáculo" and self.posicion + 1 != self.posicion_inicial:
                self.mover(1)  # Mover a la derecha

        print(f"Total de acciones realizadas: {self.acciones}")
        print(f"Total de celdas limpiadas: {self.celdas_limpiadas}")
        print(f"Eficiencia energética: {self.celdas_limpiadas / (self.acciones - self.movimientos)} celdas limpiadas por carga.")
        print(f"Movimientos realizados: {self.movimientos}")
        print(f"Limpiezas realizadas: {self.limpiezas}")

if __name__ == "__main__":
    TAMANO_ENTORNO = 20
    num_sucias = int(input("Ingrese el número de casillas sucias: "))
    num_obstaculos = int(input("Ingrese el número de obstáculos: "))
    
    entorno = generar_entorno(TAMANO_ENTORNO, num_sucias, num_obstaculos)
    
    # Encontrar una posición inicial válida (sin obstáculos)
    posicion_inicial = random.choice([i for i in range(TAMANO_ENTORNO) if entorno[i] != "obstáculo"])
    print(f"El agente inicia en la posición {posicion_inicial}.")
    
    aspiradora = AspiradoraInteligente(entorno, posicion_inicial)
    aspiradora.ejecutar()
