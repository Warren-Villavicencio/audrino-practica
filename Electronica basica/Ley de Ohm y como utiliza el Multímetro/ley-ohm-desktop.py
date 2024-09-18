import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

"""
Calculadora de la Ley de Ohm - Aplicación de Escritorio Multiplataforma

Este script implementa una calculadora para la Ley de Ohm con una interfaz gráfica de usuario
utilizando Tkinter. La aplicación es multiplataforma y puede ejecutarse en Windows, macOS y Linux.

Características principales:
- Implementa los principios SOLID y modularidad.
- Utiliza Tkinter para la interfaz gráfica, asegurando compatibilidad multiplataforma.
- Permite calcular voltaje, corriente y resistencia según la Ley de Ohm.

Posibles modificaciones futuras:
- Agregar más cálculos relacionados con electricidad (potencia, energía, etc.).
- Implementar un sistema de guardado y carga de cálculos previos.
- Añadir gráficos para visualizar la relación entre las variables.
- Incluir un modo de tema oscuro para la interfaz.
"""

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
        if tipo == "Voltaje":
            return CalculadorVoltaje()
        elif tipo == "Corriente":
            return CalculadorCorriente()
        elif tipo == "Resistencia":
            return CalculadorResistencia()
        else:
            raise ValueError("Tipo de calculadora no válido")

class AplicacionLeyOhm(tk.Tk):
    """
    Clase principal de la aplicación que maneja la interfaz gráfica y la lógica de la calculadora.
    
    Esta clase hereda de tk.Tk para crear la ventana principal de la aplicación.
    """
    
    def __init__(self):
        super().__init__()
        
        self.title("Calculadora Ley de Ohm")
        self.geometry("400x300")
        
        self.crear_widgets()
    
    def crear_widgets(self):
        """
        Crea y coloca todos los widgets de la interfaz gráfica.
        
        Posibles modificaciones:
        - Agregar más campos para cálculos adicionales.
        - Implementar un diseño más elaborado con frames y grids.
        - Añadir iconos a los botones para mejorar la experiencia visual.
        """
        # Combobox para seleccionar el tipo de cálculo
        self.tipo_calculo = ttk.Combobox(self, values=["Voltaje", "Corriente", "Resistencia"])
        self.tipo_calculo.set("Voltaje")
        self.tipo_calculo.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        self.tipo_calculo.bind("<<ComboboxSelected>>", self.actualizar_etiquetas)
        
        # Etiquetas y campos de entrada
        self.etiqueta1 = ttk.Label(self, text="Corriente (A):")
        self.etiqueta1.grid(row=1, column=0, pady=5, padx=10, sticky="e")
        self.entrada1 = ttk.Entry(self)
        self.entrada1.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        
        self.etiqueta2 = ttk.Label(self, text="Resistencia (Ω):")
        self.etiqueta2.grid(row=2, column=0, pady=5, padx=10, sticky="e")
        self.entrada2 = ttk.Entry(self)
        self.entrada2.grid(row=2, column=1, pady=5, padx=10, sticky="ew")
        
        # Botón de cálculo
        self.boton_calcular = ttk.Button(self, text="Calcular", command=self.calcular)
        self.boton_calcular.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Etiqueta para mostrar el resultado
        self.resultado = ttk.Label(self, text="")
        self.resultado.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Configurar el grid para que se expanda correctamente
        self.grid_columnconfigure(1, weight=1)
    
    def actualizar_etiquetas(self, event):
        """
        Actualiza las etiquetas de los campos de entrada según el tipo de cálculo seleccionado.
        """
        tipo = self.tipo_calculo.get()
        if tipo == "Voltaje":
            self.etiqueta1.config(text="Corriente (A):")
            self.etiqueta2.config(text="Resistencia (Ω):")
        elif tipo == "Corriente":
            self.etiqueta1.config(text="Voltaje (V):")
            self.etiqueta2.config(text="Resistencia (Ω):")
        else:  # Resistencia
            self.etiqueta1.config(text="Voltaje (V):")
            self.etiqueta2.config(text="Corriente (A):")
    
    def calcular(self):
        """
        Realiza el cálculo basado en el tipo seleccionado y los valores ingresados.
        
        Posibles modificaciones:
        - Agregar validación más robusta de la entrada del usuario.
        - Implementar manejo de errores más detallado.
        - Añadir la opción de guardar el resultado en un archivo o base de datos.
        """
        try:
            tipo = self.tipo_calculo.get()
            valor1 = float(self.entrada1.get())
            valor2 = float(self.entrada2.get())
            
            calculadora = FabricaCalculadoraOhm.crear_calculadora(tipo)
            resultado = calculadora.calcular(valor1, valor2)
            
            unidad = "V" if tipo == "Voltaje" else "A" if tipo == "Corriente" else "Ω"
            self.resultado.config(text=f"{tipo}: {resultado:.2f} {unidad}")
        except ValueError as e:
            self.resultado.config(text="Error: Ingrese valores numéricos válidos")
        except Exception as e:
            self.resultado.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    app = AplicacionLeyOhm()
    app.mainloop()
