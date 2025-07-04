import flet as ft
import requests

BACKEND_URL = "http://localhost:8000/factor"

def main(page: ft.Page):
    page.title = "Factorización Cuántica"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input_number = ft.TextField(label="Número a factorizar", width=300)
    output_text = ft.Text(value="", selectable=True, size=14)

    def on_click(e):
        numero_str = input_number.value.strip()

        if not numero_str.isdigit():
            output_text.value = "❌ Ingresa un número válido entero positivo"
            page.update()
            return

        number = int(numero_str)
        output_text.value = f"🔄 Buscando factores de {number}..."
        page.update()

        try:
            response = requests.post(BACKEND_URL, json={"number": number})
            if response.status_code == 200:
                data = response.json()
                factors = data.get("factors", [])
                method = data.get("method", "desconocido")
                error = data.get("error", None)

                if factors:
                    output_text.value = f"✅ Factores de {number}: {factors} \n🔬 Método: {method}"
                else:
                    if error:
                        output_text.value = f"⚠️ No se encontraron factores cuánticos.\n🧪 Error: {error}"
                    else:
                        output_text.value = f"⚠️ No se encontraron factores para {number}"
            else:
                output_text.value = f"❌ Error del servidor: {response.text}"
        except Exception as ex:
            output_text.value = f"⚠️ Error de conexión: {str(ex)}"

        page.update()

    submit_button = ft.ElevatedButton(text="Procesar", on_click=on_click)

    page.add(
        ft.Column(
            [
                ft.Text("🧠 Simulación Algoritmo de Shor", size=20, weight=ft.FontWeight.BOLD),
                input_number,
                submit_button,
                output_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
