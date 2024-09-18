# ley_ohm.py

"""
Este módulo implementa una calculadora para la Ley de Ohm siguiendo los principios SOLID,
código limpio y modularidad.

La Ley de Ohm establece la relación entre voltaje (V), corriente (I) y resistencia (R):
V = I * R

Principios SOLID aplicados:
- SRP (Principio de Responsabilidad Única): Cada clase tiene una única responsabilidad.
- OCP (Principio Abierto/Cerrado): Fácilmente extensible para nuevos tipos de cálculos.
- LSP (Principio de Sustitución de Liskov): Las subclases pueden sustituir a la clase base.
- ISP (Principio de Segregación de Interfaces): Interface simple para todas las calculadoras.
- DIP (Principio de Inversión de Dependencias): Dependencias basadas en abstracciones.

Posibles modificaciones futuras:
- Agregar más tipos de cálculos relacionados con electricidad.
- Implementar una interfaz gráfica de usuario (GUI).
- Añadir funcionalidad para guardar y cargar resultados.
- Incluir unidades de medida y conversiones entre ellas.
"""

from abc import ABC, abstractmethod

class CalculadoraOhm(ABC):
    """
    Clase base abstracta para todas las calculadoras de la Ley de Ohm.
    
    Esta clase define la interfaz común para todos los tipos de cálculos.
    Siguiendo el principio ISP, mantenemos esta interfaz simple y enfocada.
    """
    
    @abstractmethod
    def calcular(self, *args):
        """
        Método abstracto para realizar el cálculo.
        
        Cada subclase debe implementar este método según su tipo de cálculo específico.
        """
        pass

class CalculadorVoltaje(CalculadoraOhm):
    """
    Calcula el voltaje usando la Ley de Ohm: V = I * R
    """
    def calcular(self, corriente: float, resistencia: float) -> float:
        """
        Calcula el voltaje dada la corriente y la resistencia.
        
        :param corriente: Corriente en amperios (A)
        :param resistencia: Resistencia en ohmios (Ω)
        :return: Voltaje en voltios (V)
        """
        return corriente * resistencia

class CalculadorCorriente(CalculadoraOhm):
    """
    Calcula la corriente usando la Ley de Ohm: I = V / R
    """
    def calcular(self, voltaje: float, resistencia: float) -> float:
        """
        Calcula la corriente dado el voltaje y la resistencia.
        
        :param voltaje: Voltaje en voltios (V)
        :param resistencia: Resistencia en ohmios (Ω)
        :return: Corriente en amperios (A)
        """
        return voltaje / resistencia

class CalculadorResistencia(CalculadoraOhm):
    """
    Calcula la resistencia usando la Ley de Ohm: R = V / I
    """
    def calcular(self, voltaje: float, corriente: float) -> float:
        """
        Calcula la resistencia dado el voltaje y la corriente.
        
        :param voltaje: Voltaje en voltios (V)
        :param corriente: Corriente en amperios (A)
        :return: Resistencia en ohmios (Ω)
        """
        return voltaje / corriente

class FabricaCalculadoraOhm:
    """
    Fábrica para crear instancias de calculadoras de la Ley de Ohm.
    
    Esta clase implementa el patrón de diseño Factory, permitiendo la creación
    de diferentes tipos de calculadoras sin exponer la lógica de instanciación.
    
    Posible modificación: Agregar más tipos de calculadoras relacionadas con electricidad.
    """
    
    @staticmethod
    def crear_calculadora(tipo: str) -> CalculadoraOhm:
        """
        Crea y retorna una instancia de la calculadora especificada.
        
        :param tipo: Tipo de calculadora a crear ("voltaje", "corriente", o "resistencia")
        :return: Instancia de la calculadora correspondiente
        :raises ValueError: Si se proporciona un tipo de calculadora no válido
        """
        if tipo == "voltaje":
            return CalculadorVoltaje()
        elif tipo == "corriente":
            return CalculadorCorriente()
        elif tipo == "resistencia":
            return CalculadorResistencia()
        else:
            raise ValueError("Tipo de calculadora no válido")

def mostrar_menu():
    """
    Muestra el menú principal de la aplicación.
    
    Posible modificación: Agregar más opciones al menú para funcionalidades adicionales.
    """
    print("\nCalculadora de la Ley de Ohm")
    print("1. Calcular Voltaje")
    print("2. Calcular Corriente")
    print("3. Calcular Resistencia")
    print("4. Salir")

def obtener_entrada(mensaje: str) -> float:
    """
    Solicita y valida la entrada del usuario para valores numéricos.
    
    :param mensaje: Mensaje a mostrar al usuario
    :return: Valor numérico ingresado por el usuario
    
    Posible modificación: Agregar validación de rango para los valores ingresados.
    """
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Por favor, ingrese un número válido.")

def main():
    """
    Función principal que ejecuta la lógica de la aplicación.
    
    Esta función maneja el flujo principal del programa, incluyendo la interacción
    con el usuario y la ejecución de los cálculos.
    
    Posibles modificaciones:
    - Implementar manejo de errores más robusto.
    - Agregar opciones para guardar resultados en un archivo.
    - Integrar con una base de datos para almacenar historial de cálculos.
    """
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
