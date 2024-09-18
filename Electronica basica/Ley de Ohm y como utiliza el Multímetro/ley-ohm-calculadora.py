# ley_ohm.py

from abc import ABC, abstractmethod

class CalculadoraOhm(ABC):
    @abstractmethod
    def calcular(self, *args):
        pass

class CalculadorVoltaje(CalculadoraOhm):
    def calcular(self, corriente: float, resistencia: float) -> float:
        return corriente * resistencia

class CalculadorCorriente(CalculadoraOhm):
    def calcular(self, voltaje: float, resistencia: float) -> float:
        return voltaje / resistencia

class CalculadorResistencia(CalculadoraOhm):
    def calcular(self, voltaje: float, corriente: float) -> float:
        return voltaje / corriente

class FabricaCalculadoraOhm:
    @staticmethod
    def crear_calculadora(tipo: str) -> CalculadoraOhm:
        if tipo == "voltaje":
            return CalculadorVoltaje()
        elif tipo == "corriente":
            return CalculadorCorriente()
        elif tipo == "resistencia":
            return CalculadorResistencia()
        else:
            raise ValueError("Tipo de calculadora no válido")

def mostrar_menu():
    print("\nCalculadora de la Ley de Ohm")
    print("1. Calcular Voltaje")
    print("2. Calcular Corriente")
    print("3. Calcular Resistencia")
    print("4. Salir")

def obtener_entrada(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Por favor, ingrese un número válido.")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-4): ")

        if opcion == "4":
            print("Gracias por usar la calculadora de la Ley de Ohm. ¡Hasta luego!")
            break

        if opcion in ["1", "2", "3"]:
            if opcion == "1":
                tipo = "voltaje"
                valor1 = obtener_entrada("Ingrese la corriente (en amperios): ")
                valor2 = obtener_entrada("Ingrese la resistencia (en ohmios): ")
            elif opcion == "2":
                tipo = "corriente"
                valor1 = obtener_entrada("Ingrese el voltaje (en voltios): ")
                valor2 = obtener_entrada("Ingrese la resistencia (en ohmios): ")
            else:
                tipo = "resistencia"
                valor1 = obtener_entrada("Ingrese el voltaje (en voltios): ")
                valor2 = obtener_entrada("Ingrese la corriente (en amperios): ")

            calculadora = FabricaCalculadoraOhm.crear_calculadora(tipo)
            resultado = calculadora.calcular(valor1, valor2)

            print(f"El resultado del cálculo de {tipo} es: {resultado:.2f}")
        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")

if __name__ == "__main__":
    main()
