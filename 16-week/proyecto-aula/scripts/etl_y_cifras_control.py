"""
Replica en Python las mismas reglas del ETL de Power Query para obtener las cifras de control
con las que se valida el tablero. Uso: python etl_y_cifras_control.py <carpeta_datos_crudos>
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

d = Path(sys.argv[1])
raw = pd.read_csv(d / "control_lechero.csv", sep=";", dtype=str)
fin = pd.read_excel(d / "maestros_ganadera.xlsx", sheet_name="Fincas")
ani = pd.read_excel(d / "maestros_ganadera.xlsx", sheet_name="Animales")
pre = pd.read_csv(d / "precios_leche.csv")

print("Filas crudas:", len(raw))
h = raw.drop_duplicates()
print("Sin duplicados:", len(h), "(eliminadas", len(raw) - len(h), ")")
h = h.drop(columns="Finca")
h["Fecha"] = [pd.to_datetime(f, format="%d/%m/%Y") if "/" in f else pd.to_datetime(f, format="%Y-%m-%d") for f in h.Fecha]
h["Fecha"] = pd.to_datetime(h.Fecha)
print("Rango fechas:", h.Fecha.min().date(), "-", h.Fecha.max().date())
h["LitrosDia"] = pd.to_numeric(h.LitrosDia.str.replace(",", "."), errors="coerce")
print("Litros vacíos:", h.LitrosDia.isna().sum(), " Litros >30 corregidos:", (h.LitrosDia > 30).sum())
h = h[h.LitrosDia.notna()].copy()
h.loc[h.LitrosDia > 30, "LitrosDia"] = h.LitrosDia / 10
for c in ["SuplementoKg", "CostoSuplemento", "DiasEnLeche"]:
    h[c] = pd.to_numeric(h[c])
h["AnioMes"] = h.Fecha.dt.strftime("%Y-%m")
h = h.merge(pre, on="AnioMes", how="left")
h["IngresoSemanal"] = h.LitrosDia * 7 * h.PrecioLitro
print("Filas finales hechos:", len(h))

def raza_ok(r):
    r = r.strip().lower().replace("cebu", "cebú")
    return {"gyr": "Gyr", "gir": "Gyr", "girolando": "Girolando",
            "f1 holstein x cebú": "F1 Holstein x Cebú", "simmental x cebú": "Simmental x Cebú"}[r]
print("Variantes de raza antes:", sorted(ani.Raza.unique()))
ani["Raza"] = ani.Raza.map(raza_ok)
print("Razas después:", ani.Raza.value_counts().to_dict())

h = h.merge(ani[["IdAnimal", "Raza"]], on="IdAnimal").merge(fin[["IdFinca", "Finca", "Municipio"]], on="IdFinca")
m = h.Fecha.dt.month; y = h.Fecha.dt.year
h["Epoca"] = np.where(m.isin([12, 1, 2, 7, 8, 9]), "Seca", "Lluvias")
h["Temporada"] = np.select(
    [m.isin([7, 8, 9]), m.isin([12, 1, 2]), m.isin([3, 4, 5])],
    ["Seca jul-sep", "Seca dic-feb", "Lluvias mar-may"], "Lluvias oct-nov / jun")

kpi = lambda x: x.LitrosDia.sum() / len(x)
fmt = lambda v: f"{v:,.2f}"
print("\n=== MEDIDAS (total) ===")
print("Controles:", len(h), " Vacas distintas:", h.IdAnimal.nunique())
print("Litros registrados:", fmt(h.LitrosDia.sum()))
print("KPI L/vaca/día:", fmt(kpi(h)))
print("Costo suplemento por litro:", fmt(h.CostoSuplemento.sum() / h.LitrosDia.sum()))
print("Ingreso estimado:", fmt(h.IngresoSemanal.sum()))
print("% controles bajo 6 L:", fmt(100 * (h.LitrosDia < 6).mean()))
print("Precio promedio:", fmt(h.PrecioLitro.mean()))

print("\n=== KPI por año / temporada ===")
s26 = (y == 2026) & m.isin([7, 8, 9]); l26 = (y == 2026) & m.isin([3, 4, 5]); s25 = (y == 2025) & m.isin([7, 8, 9])
print("Seca jul-sep 2026:", fmt(kpi(h[s26])), " Lluvias mar-may 2026:", fmt(kpi(h[l26])),
      " Seca jul-sep 2025:", fmt(kpi(h[s25])))
print("Caída vs lluvias %:", fmt(100 * (kpi(h[s26]) / kpi(h[l26]) - 1)),
      " vs 2025 %:", fmt(100 * (kpi(h[s26]) / kpi(h[s25]) - 1)))
print(h.groupby(h.Fecha.dt.to_period("M")).apply(kpi).round(2).to_string())

print("\n=== Por finca: lluvias 26 vs seca 26 ===")
for g in ["Finca", "Raza"]:
    t = pd.DataFrame({"Lluvias": h[l26].groupby(g).apply(kpi), "Seca": h[s26].groupby(g).apply(kpi),
                      "Seca25": h[s25].groupby(g).apply(kpi), "Ctrl_seca": h[s26].groupby(g).size()})
    t["Caida%"] = 100 * (t.Seca / t.Lluvias - 1)
    print(t.round(2).sort_values("Caida%"))

# Litros perdidos aditivo por Finca x Raza (igual que la medida DAX con SUMX)
gl = h[l26].groupby(["Finca", "Raza"]).apply(kpi).rename("KL")
gs = h[s26].groupby(["Finca", "Raza"]).agg(KS=("LitrosDia", lambda s: s.mean()), N=("LitrosDia", "size"))
t = gs.join(gl)
t["Perdidos"] = (t.KL - t.KS).clip(lower=0) * t.N * 7
precio_seca = h[s26].PrecioLitro.mean()
t["Ingreso"] = t.Perdidos * precio_seca
tot = t.Perdidos.sum()
print("\nPrecio promedio seca 2026:", fmt(precio_seca))
print("LITROS PERDIDOS seca 2026:", fmt(tot), " INGRESO PERDIDO:", fmt(tot * precio_seca))
print((t.assign(Part=100 * t.Perdidos / tot).round(1)).sort_values("Perdidos", ascending=False).to_string())
print("Por finca:", (t.groupby("Finca").Perdidos.sum() / tot * 100).round(1).to_dict())
print("Por raza:", (t.groupby("Raza").Perdidos.sum() / tot * 100).round(1).to_dict())
ced = t.loc["El Cedral"].Perdidos.sum() + t.loc["La Esperanza"].Perdidos.sum()
print("Norte (Cedral+Esperanza) %:", round(100 * ced / tot, 1))
hx = t.xs("F1 Holstein x Cebú", level="Raza").Perdidos.sum()
print("HxC %:", round(100 * hx / tot, 1))
print("Cedral+HxC %:", round(100 * t.loc[("El Cedral", "F1 Holstein x Cebú")].Perdidos / tot, 1))

print("\n=== Prueba del clic ===")
print("1) Finca = El Cedral (todo el periodo):", fmt(kpi(h[h.Finca == "El Cedral"])), "controles", (h.Finca == "El Cedral").sum())
print("2) Raza = F1 Holstein x Cebú:", fmt(kpi(h[h.Raza == "F1 Holstein x Cebú"])), "controles", (h.Raza == "F1 Holstein x Cebú").sum())
sel = h[s26 & (h.Finca == "El Cedral") & (h.Raza == "F1 Holstein x Cebú")]
print("3) Seca jul-sep 2026 + El Cedral + HxC:", fmt(kpi(sel)), "controles", len(sel))
print("Suplemento kg promedio seca26 por finca:", h[s26].groupby("Finca").SuplementoKg.mean().round(2).to_dict())
print("Costo sup/litro seca26 por finca:", (h[s26].groupby("Finca").CostoSuplemento.sum()/h[s26].groupby("Finca").LitrosDia.sum()).round(0).to_dict())
h.to_csv(d.parent / "_hechos_limpios_ref.csv", index=False)
