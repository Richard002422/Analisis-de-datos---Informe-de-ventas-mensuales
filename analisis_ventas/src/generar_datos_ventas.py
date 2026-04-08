from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path


def generar_datos_sinteticos(
    n_registros: int = 500,
    fecha_inicio: date = date(2025, 1, 1),
    fecha_fin: date = date(2025, 12, 31),
    semilla: int = 42,
) -> list[dict[str, object]]:
    random.seed(semilla)

    productos = [
        "Laptop",
        "Mouse",
        "Teclado",
        "Monitor",
        "Auriculares",
        "Webcam",
        "Impresora",
        "Tablet",
    ]

    dias_rango = (fecha_fin - fecha_inicio).days
    datos: list[dict[str, object]] = []

    for _ in range(n_registros):
        fecha = fecha_inicio + timedelta(days=random.randint(0, dias_rango))
        producto = random.choice(productos)
        cantidad = random.randint(1, 20)

        # Rango de precios por producto para simular realismo.
        if producto == "Laptop":
            precio = round(random.uniform(650, 1800), 2)
        elif producto == "Monitor":
            precio = round(random.uniform(120, 600), 2)
        elif producto == "Tablet":
            precio = round(random.uniform(180, 900), 2)
        elif producto == "Impresora":
            precio = round(random.uniform(90, 450), 2)
        else:
            precio = round(random.uniform(12, 180), 2)

        datos.append(
            {
                "fecha": fecha.isoformat(),
                "producto": producto,
                "cantidad": cantidad,
                "precio": precio,
            }
        )

    return datos


def guardar_csv(datos: list[dict[str, object]], ruta_salida: Path) -> None:
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    with ruta_salida.open("w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(
            archivo, fieldnames=["fecha", "producto", "cantidad", "precio"]
        )
        writer.writeheader()
        writer.writerows(datos)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    salida = root / "data" / "ventas_sinteticas.csv"

    registros = generar_datos_sinteticos()
    guardar_csv(registros, salida)

    print(f"Archivo generado: {salida}")
    print(f"Registros: {len(registros)}")
