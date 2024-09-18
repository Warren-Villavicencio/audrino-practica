# Estructura del proyecto Django:
#
# ley_ohm_proyecto/
# ├── ley_ohm_proyecto/
# │   ├── __init__.py
# │   ├── settings.py
# │   ├── urls.py
# │   └── wsgi.py
# ├── calculadora/
# │   ├── __init__.py
# │   ├── admin.py
# │   ├── apps.py
# │   ├── models.py
# │   ├── tests.py
# │   ├── urls.py
# │   ├── views.py
# │   └── templates/
# │       └── calculadora/
# │           └── index.html
# ├── static/
# │   └── css/
# │       └── style.css
# └── manage.py

# Primero, creamos el archivo views.py en la aplicación 'calculadora'

# calculadora/views.py
from django.shortcuts import render
from django.http import JsonResponse
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

def index(request):
    return render(request, 'calculadora/index.html')

def calcular(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        valor1 = float(request.POST.get('valor1', 0))
        valor2 = float(request.POST.get('valor2', 0))

        try:
            calculadora = FabricaCalculadoraOhm.crear_calculadora(tipo)
            resultado = calculadora.calcular(valor1, valor2)
            return JsonResponse({'resultado': f"{resultado:.2f}"})
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Ahora, creamos el archivo urls.py en la aplicación 'calculadora'

# calculadora/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calcular/', views.calcular, name='calcular'),
]

# Luego, actualizamos el archivo urls.py del proyecto principal

# ley_ohm_proyecto/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('calculadora.urls')),
]

# Ahora, creamos el template HTML para la interfaz de usuario

# calculadora/templates/calculadora/index.html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora Ley de Ohm</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <div class="container">
        <h1>Calculadora de la Ley de Ohm</h1>
        <form id="ohm-form">
            <select id="tipo" name="tipo">
                <option value="voltaje">Calcular Voltaje</option>
                <option value="corriente">Calcular Corriente</option>
                <option value="resistencia">Calcular Resistencia</option>
            </select>
            <div id="input-fields">
                <input type="number" id="valor1" name="valor1" step="any" required>
                <input type="number" id="valor2" name="valor2" step="any" required>
            </div>
            <button type="submit">Calcular</button>
        </form>
        <div id="resultado"></div>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const form = document.getElementById('ohm-form');
            const tipoSelect = document.getElementById('tipo');
            const inputFields = document.getElementById('input-fields');
            const resultadoDiv = document.getElementById('resultado');

            tipoSelect.addEventListener('change', updateLabels);
            form.addEventListener('submit', calcular);

            function updateLabels() {
                const tipo = tipoSelect.value;
                let label1, label2;
                switch (tipo) {
                    case 'voltaje':
                        label1 = 'Corriente (A)';
                        label2 = 'Resistencia (Ω)';
                        break;
                    case 'corriente':
                        label1 = 'Voltaje (V)';
                        label2 = 'Resistencia (Ω)';
                        break;
                    case 'resistencia':
                        label1 = 'Voltaje (V)';
                        label2 = 'Corriente (A)';
                        break;
                }
                inputFields.innerHTML = `
                    <input type="number" id="valor1" name="valor1" placeholder="${label1}" step="any" required>
                    <input type="number" id="valor2" name="valor2" placeholder="${label2}" step="any" required>
                `;
            }

            function calcular(e) {
                e.preventDefault();
                const formData = new FormData(form);
                fetch('/calcular/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        resultadoDiv.textContent = `Error: ${data.error}`;
                    } else {
                        const tipo = tipoSelect.value.charAt(0).toUpperCase() + tipoSelect.value.slice(1);
                        const unidad = tipo === 'Voltaje' ? 'V' : tipo === 'Corriente' ? 'A' : 'Ω';
                        resultadoDiv.textContent = `${tipo}: ${data.resultado} ${unidad}`;
                    }
                })
                .catch(error => {
                    resultadoDiv.textContent = `Error: ${error}`;
                });
            }

            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            updateLabels();
        });
    </script>
</body>
</html>

# Finalmente, creamos un archivo CSS para estilizar la página

# static/css/style.css
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}

.container {
    width: 80%;
    margin: auto;
    overflow: hidden;
    padding: 20px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    margin-top: 50px;
}

h1 {
    color: #333;
    text-align: center;
}

form {
    display: flex;
    flex-direction: column;
    align-items: center;
}

select, input, button {
    margin: 10px 0;
    padding: 10px;
    width: 100%;
    max-width: 300px;
}

button {
    background-color: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}

#resultado {
    margin-top: 20px;
    font-weight: bold;
    text-align: center;
}

#input-fields {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}
