import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
import sys
import os

"""
Calculadora de la Ley de Ohm - Aplicación de Escritorio para Windows

Este script implementa una calculadora para la Ley de Ohm con una interfaz gráfica de usuario
utilizando Tkinter, optimizada para crear un ejecutable para Windows.

Características principales:
- Implementa los principios SOLID y modularidad.
- Utiliza Tkinter para la interfaz gráfica.
- Diseñado para ser empaquetado como un ejecutable de Windows usando PyInstaller.

Instrucciones para crear el ejecutable:
1. Instala PyInstaller: pip install pyinstaller
2. Ejecuta: pyinstaller --onefile --windowed --name=CalculadoraLeyOhm --icon=icono.ico calculadora_ley_ohm.py

Nota: Asegúrate de tener un archivo icono.ico en el mismo directorio para el ícono de la aplicación.

Posibles modificaciones futuras:
- Agregar más cálculos relacionados con electricidad (potencia, energía, etc.).
- Implementar un sistema de guardado y carga de cálculos previos.
- Añadir gráficos para visualizar la relación entre las variables.
- Incluir un modo de tema oscuro para la interfaz.
"""

# [Las clases CalculadoraOhm, CalculadorVoltaje, CalculadorCorriente, CalculadorResistencia y FabricaCalculadoraOhm 
# permanecen sin cambios, por lo que se han omitido para brevedad]

class AplicacionLeyOhm(tk.Tk):
    """
    Clase principal de la aplicación que maneja la interfaz gráfica y la lógica de la calculadora.
    
    Esta clase hereda de tk.Tk para crear la ventana principal de la aplicación.
    """
    
    def __init__(self):
        super().__init__()
        
        self.title("Calculadora Ley de Ohm")
        self.geometry("400x300")
        self.configure(bg='#f0f0f0')  # Color de fondo para toda la aplicación
        
        # Centrar la ventana en la pantalla
        self.center_window()
        
        # Establecer el ícono de la aplicación
        if getattr(sys, 'frozen', False):
            # Si es un ejecutable creado por PyInstaller
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(application_path, "icono.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        
        self.crear_widgets()
    
    def center_window(self):
        """
        Centra la ventana en la pantalla.
        """
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def crear_widgets(self):
        """
        Crea y coloca todos los widgets de la interfaz gráfica.
        
        Posibles modificaciones:
        - Agregar más campos para cálculos adicionales.
        - Implementar un diseño más elaborado con frames y grids.
        - Añadir iconos a los botones para mejorar la experiencia visual.
        """
        style = ttk.Style()
        style.theme_use('clam')  # Usar un tema más moderno
        
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Combobox para seleccionar el tipo de cálculo
        self.tipo_calculo = ttk.Combobox(main_frame, values=["Voltaje", "Corriente", "Resistencia"], state="readonly")
        self.tipo_calculo.set("Voltaje")
        self.tipo_calculo.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        self.tipo_calculo.bind("<<ComboboxSelected>>", self.actualizar_etiquetas)
        
        # Etiquetas y campos de entrada
        self.etiqueta1 = ttk.Label(main_frame, text="Corriente (A):")
        self.etiqueta1.grid(row=1, column=0, pady=5, padx=10, sticky="e")
        self.entrada1 = ttk.Entry(main_frame)
        self.entrada1.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        
        self.etiqueta2 = ttk.Label(main_frame, text="Resistencia (Ω):")
        self.etiqueta2.grid(row=2, column=0, pady=5, padx=10, sticky="e")
        self.entrada2 = ttk.Entry(main_frame)
        self.entrada2.grid(row=2, column=1, pady=5, padx=10, sticky="ew")
        
        # Botón de cálculo
        self.boton_calcular = ttk.Button(main_frame, text="Calcular", command=self.calcular)
        self.boton_calcular.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Etiqueta para mostrar el resultado
        self.resultado = ttk.Label(main_frame, text="", font=('Arial', 12, 'bold'))
        self.resultado.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Configurar el grid para que se expanda correctamente
        main_frame.grid_columnconfigure(1, weight=1)
    
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
        except ValueError:
            self.resultado.config(text="Error: Ingrese valores numéricos válidos")
        except Exception as e:
            self.resultado.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    app = AplicacionLeyOhm()
    app.mainloop()
