from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "data" / "ventas_sinteticas.csv"
    reports_dir = base_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # 1. Cargar datos del CSV
    df = pd.read_csv(data_path)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["total"] = df["cantidad"] * df["precio"]
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)

    # 2. Calcular ventas totales por mes
    ventas_por_mes = (
        df.groupby("mes", as_index=False)["total"]
        .sum()
        .sort_values("mes")
    )

    ventas_por_producto = (
        df.groupby("producto", as_index=False)["cantidad"]
        .sum()
        .sort_values("cantidad", ascending=False)
    )

    ingresos_por_producto = (
        df.groupby("producto", as_index=False)["total"]
        .sum()
        .sort_values("total", ascending=False)
    )

    # 3. Determinar producto mas vendido y con mayor ingresos
    producto_mas_vendido = ventas_por_producto.iloc[0]
    producto_mayor_ingreso = ingresos_por_producto.iloc[0]

    print("Ventas totales por mes:")
    print(ventas_por_mes, "\n")
    print(
        f"Producto mas vendido (unidades): {producto_mas_vendido['producto']} "
        f"({int(producto_mas_vendido['cantidad'])} unidades)"
    )
    print(
        f"Producto con mayor ingresos: {producto_mayor_ingreso['producto']} "
        f"(${producto_mayor_ingreso['total']:,.2f})\n"
    )
    print(f"Total general vendido: ${df['total'].sum():,.2f}")

    # 4. Graficar ventas por mes
    plt.figure(figsize=(10, 5))
    plt.plot(ventas_por_mes["mes"], ventas_por_mes["total"], marker="o")
    plt.title("Ventas totales por mes")
    plt.xlabel("Mes")
    plt.ylabel("Total vendido")
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    ruta_ventas_mes = reports_dir / "ventas_por_mes.png"
    plt.savefig(ruta_ventas_mes, dpi=150)

    # 5. Graficar top 5 productos por ingresos
    top5 = ingresos_por_producto.head(5)
    plt.figure(figsize=(10, 5))
    plt.bar(top5["producto"], top5["total"])
    plt.title("Top 5 productos por ingresos")
    plt.xlabel("Producto")
    plt.ylabel("Ingresos")
    plt.xticks(rotation=30)
    plt.tight_layout()
    ruta_top5 = reports_dir / "top_5_productos_ingresos.png"
    plt.savefig(ruta_top5, dpi=150)

    plt.show()
    print(f"Grafica guardada: {ruta_ventas_mes}")
    print(f"Grafica guardada: {ruta_top5}")


if __name__ == "__main__":
    main()
