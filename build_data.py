# -*- coding: utf-8 -*-
"""
build_data.py - Convierte BBDD_Hogar.xlsx (hoja "Historico") en data.json
para el panel web de Encuestas de Calidad - Hogar.

Uso:
    python build_data.py BBDD_Hogar.xlsx

Requiere:
    pip install openpyxl
"""
import sys
import json
from datetime import datetime

try:
    import openpyxl
except ImportError:
    print("Falta la libreria openpyxl. Instalala con: pip install openpyxl")
    sys.exit(1)

MESES_ES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def norm(v):
    if v is None:
        return ""
    return str(v).strip()


def norm_upper(v):
    return norm(v).upper()


def estado_encuesta_canon(estado):
    """Unifica variantes de mayus/minus del Estado de encuesta a una forma legible."""
    e = norm_upper(estado)
    mapa = {
        "ENCUESTA REALIZADA": "Encuesta Realizada",
        "ENCUESTA PENDIENTE": "Encuesta Pendiente",
        "PARCIAL": "Parcial",
        "NO ENTREVISTAR": "No entrevistar",
        "INTERNO CARDINAL": "Interno Cardinal",
    }
    return mapa.get(e, norm(estado) or "Sin dato")


def clasif_recomendacion(valor):
    v = norm_upper(valor)
    if "NO RECOMIENDA" in v:
        return "detractor"
    if "RECOMIENDA" in v:
        return "promotor"
    if "NO OPINA" in v:
        return "pasivo"
    return None


def mes_label(dt):
    if not isinstance(dt, datetime):
        s = norm(dt)
        return s if s else None
    return f"{MESES_ES[dt.month - 1]}-{str(dt.year)[2:]}"


def mes_orden_val(dt):
    if not isinstance(dt, datetime):
        return 0
    return dt.year * 100 + dt.month


def num_1_5(v):
    if isinstance(v, (int, float)) and 1 <= v <= 5:
        return int(v) if float(v).is_integer() else round(v, 2)
    return None


def main():
    if len(sys.argv) < 2:
        print("Uso: python build_data.py <archivo.xlsx>")
        sys.exit(1)

    path = sys.argv[1]
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Histórico"]

    IDX = {
        "mes": 0, "area": 1, "cia": 2, "campania": 3, "provincia": 4,
        "servicio": 5, "prestador": 15, "gestion_tel": 23,
        "estado_encuesta": 24, "atencion": 25, "trabajo": 26,
        "recomendacion": 27, "comentario": 28,
    }

    registros = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None and row[8] is None:
            continue
        mes = row[IDX["mes"]]
        registros.append({
            "mes": mes_label(mes),
            "mes_orden": mes_orden_val(mes),
            "area": norm(row[IDX["area"]]) or "Sin dato",
            "cia": norm(row[IDX["cia"]]) or "Sin dato",
            "provincia": norm(row[IDX["provincia"]]) or "Sin dato",
            "servicio": norm(row[IDX["servicio"]]) or "Sin dato",
            "prestador": norm(row[IDX["prestador"]]) or "Sin dato",
            "gestion_tel": norm(row[IDX["gestion_tel"]]) or "Sin dato",
            "estado_encuesta": estado_encuesta_canon(row[IDX["estado_encuesta"]]),
            "atencion": num_1_5(row[IDX["atencion"]]),
            "trabajo": num_1_5(row[IDX["trabajo"]]),
            "recomendacion": clasif_recomendacion(row[IDX["recomendacion"]]),
            "comentario": norm(row[IDX["comentario"]]),
        })

    data = {
        "generado": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "registros": registros,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=0, separators=(",", ":"))

    print(f"OK -> data.json generado con {len(registros)} casos")


if __name__ == "__main__":
    main()
