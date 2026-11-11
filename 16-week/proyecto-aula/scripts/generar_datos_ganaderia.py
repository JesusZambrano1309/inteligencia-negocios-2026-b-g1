"""
Generador de datos sintéticos — Ganadera San Isidro del Huila S.A.S. (empresa ficticia)
Proyecto de aula, Inteligencia de Negocios 2026-B, CORHUILA.
Integrantes: Jesús Anibal Zambrano Orjuela y Danna Camila Cuevas.

Genera tres fuentes con formatos distintos, como llegarían de la empresa:
  1. control_lechero.csv   -> exportación del software de registro de ordeño (hechos)
  2. maestros_ganadera.xlsx -> hojas Fincas, Animales, Potreros (dimensiones)
  3. precios_leche.csv     -> liquidación mensual de la planta acopiadora

Reglas de realismo (documentadas en el README):
  - Curva de lactancia de Wood: y(t) = a * t^0.2 * e^(-0.004 t); pico cerca del día 50.
  - Producción pico según raza: Gyr 8, Girolando 10, F1 Holstein x Cebú 11.5, Simmental x Cebú 9 L.
  - Primera lactancia produce 15 % menos; variación individual de +/-12 %.
  - Intervalo entre partos ~430 días; lactancia de 270 a 300 días; control lechero semanal.
  - Huila tiene dos épocas secas: dic-feb (moderada) y jul-sep (fuerte).
    La época seca jul-sep de 2026 fue más intensa que la de 2025.
  - El efecto de la sequía depende de la finca (altitud y riego) y de la raza
    (el Holstein x Cebú tolera peor el calor; el Gyr lo tolera mejor).
  - La empresa reparte el suplemento igual en todas las fincas (~2 kg/vaca/día; ~2,5 kg en seca).
  - Precio de la leche: tendencia al alza de ~1.880 a ~2.080 COP/L con ruido mensual.

Problemas de calidad introducidos a propósito (para el ETL):
  P1. Filas duplicadas (~2 %) por doble exportación.
  P2. Fechas en dos formatos: dd/mm/aaaa y aaaa-mm-dd.
  P3. Litros con coma decimal ("8,5") y errores de digitación x10 (85 en vez de 8,5); algunos vacíos.
  P4. Razas y nombres de finca escritos de varias formas (mayúsculas, tildes, espacios, "Gir").
Uso: python generar_datos_ganaderia.py <carpeta_salida>
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1309)

INICIO, FIN = pd.Timestamp("2024-11-01"), pd.Timestamp("2026-10-31")

# ---------------- Dimensión Finca ----------------
fincas = pd.DataFrame([
    # IdFinca, Finca, Municipio, Subregion, Altitud, Ha, Riego, Vacas, efecto_seca
    ["F01", "La Esperanza", "Palermo",  "Norte",  550, 180, "No", 60, 0.20],
    ["F02", "El Cedral",    "Aipe",     "Norte",  380, 210, "No", 70, 0.30],
    ["F03", "Buenavista",   "Garzón",   "Centro", 830, 140, "Sí", 50, 0.12],
    ["F04", "Los Naranjos", "Pitalito", "Sur",   1300, 120, "Sí", 45, 0.06],
], columns=["IdFinca", "Finca", "Municipio", "Subregion", "AltitudMsnm",
            "Hectareas", "Riego", "_vacas", "_efecto"])

# ---------------- Dimensión Potrero ----------------
pastos = {"F01": ["Brachiaria decumbens", "Angleton", "Estrella africana"],
          "F02": ["Brachiaria decumbens", "Angleton", "Guinea Mombasa"],
          "F03": ["Brachiaria brizantha", "Estrella africana", "Guinea Mombasa"],
          "F04": ["Kikuyo", "Brachiaria brizantha", "Estrella africana"]}
pot_rows = []
for _, f in fincas.iterrows():
    for i in range(1, 9):
        pot_rows.append([f"{f.IdFinca}-P{i:02d}", f.IdFinca, f"Potrero {i}",
                         pastos[f.IdFinca][(i - 1) % 3], round(rng.uniform(8, 25), 1)])
potreros = pd.DataFrame(pot_rows, columns=["IdPotrero", "IdFinca", "Potrero", "Pasto", "Hectareas"])

# ---------------- Dimensión Animal ----------------
razas = {"Gyr": (8.0, 0.5), "Girolando": (10.0, 0.9),
         "F1 Holstein x Cebú": (11.5, 1.4), "Simmental x Cebú": (9.0, 1.1)}
mezcla = {"F01": [0.20, 0.30, 0.35, 0.15], "F02": [0.10, 0.25, 0.50, 0.15],
          "F03": [0.25, 0.35, 0.20, 0.20], "F04": [0.15, 0.45, 0.25, 0.15]}
ani_rows, n = [], 1
for _, f in fincas.iterrows():
    for _ in range(f._vacas):
        raza = rng.choice(list(razas), p=mezcla[f.IdFinca])
        nac = INICIO - pd.Timedelta(days=int(rng.integers(3 * 365, 9 * 365)))
        partos = int(np.clip((INICIO - nac).days // 430 - 2, 1, 7))
        ani_rows.append([f"V{n:04d}", f.IdFinca, raza, nac.date(), partos,
                         float(np.clip(rng.normal(1, 0.12), 0.7, 1.3))])
        n += 1
animales = pd.DataFrame(ani_rows, columns=["IdAnimal", "IdFinca", "Raza", "FechaNacimiento",
                                           "PartosAlInicio", "_mult"])

# ---------------- Precios ----------------
meses = pd.period_range(INICIO, FIN, freq="M")
precios = pd.DataFrame({"AnioMes": [m.strftime("%Y-%m") for m in meses]})
tend = np.linspace(1880, 2080, len(meses))
precios["PrecioLitro"] = (tend + rng.normal(0, 18, len(meses))
                          + [25 if m.month in (1, 2, 7, 8, 9) else 0 for m in meses]).round()

# ---------------- Clima: severidad de la época seca ----------------
def severidad(d):
    if d.month in (7, 8, 9):
        return 1.0 if d.year == 2026 else 0.55
    if d.month in (12, 1, 2):
        return 0.40
    if d.month in (6, 10):          # transición
        return 0.15 if d.month == 6 else 0.05
    return 0.0

def costo_kg(d):
    return 1750 if d.year <= 2025 else 1900

# ---------------- Hechos: control lechero semanal ----------------
dia_control = {"F01": 1, "F02": 2, "F03": 3, "F04": 4}  # martes..viernes
efecto = fincas.set_index("IdFinca")._efecto
rows = []
for _, a in animales.iterrows():
    # fechas de parto: primer parto antes del inicio, luego cada ~430 días
    parto = INICIO - pd.Timedelta(days=int(rng.integers(0, 430)))
    partos = []
    while parto <= FIN:
        partos.append((parto, int(rng.integers(270, 301))))
        parto += pd.Timedelta(days=int(rng.normal(430, 40)))
    pico, sens = razas[a.Raza]
    a_wood = pico / (50 ** 0.2 * np.exp(-0.2))
    for k, (fp, largo) in enumerate(partos):
        primera = (a.PartosAlInicio == 1 and k == 0)
        for d in pd.date_range(max(fp + pd.Timedelta(days=5), INICIO),
                               min(fp + pd.Timedelta(days=largo), FIN)):
            if d.dayofweek != dia_control[a.IdFinca]:
                continue
            t = (d - fp).days
            base = a_wood * t ** 0.2 * np.exp(-0.004 * t) * a._mult * (0.85 if primera else 1.0)
            caida = min(0.75, severidad(d) * efecto[a.IdFinca] * sens)
            litros = max(0.8, base * (1 - caida) * rng.normal(1, 0.06))
            sup = rng.uniform(1.5, 2.5) + (0.5 if severidad(d) >= 0.4 else 0)
            rows.append([d, a.IdAnimal, a.IdFinca,
                         f"{a.IdFinca}-P{int(rng.integers(1, 9)):02d}", t,
                         round(litros, 1), round(sup, 1), round(sup * costo_kg(d))])

hechos = pd.DataFrame(rows, columns=["Fecha", "IdAnimal", "IdFinca", "IdPotrero", "DiasEnLeche",
                                     "LitrosDia", "SuplementoKg", "CostoSuplemento"])
hechos = hechos.sort_values(["Fecha", "IdAnimal"]).reset_index(drop=True)
hechos.insert(0, "IdControl", [f"C{i:06d}" for i in range(1, len(hechos) + 1)])


# ---------------- Ensuciar a propósito ----------------
sucio = hechos.copy()
nombre_finca = fincas.set_index("IdFinca").Finca
variantes_finca = {"La Esperanza": ["La Esperanza", "LA ESPERANZA", "la esperanza "],
                   "El Cedral": ["El Cedral", "EL CEDRAL", "El cedral "],
                   "Buenavista": ["Buenavista", "Buena Vista", "BUENAVISTA"],
                   "Los Naranjos": ["Los Naranjos", "LOS NARANJOS", "Los naranjos "]}
sucio.insert(3, "Finca", [rng.choice(variantes_finca[nombre_finca[i]], p=[0.8, 0.1, 0.1])
                          for i in sucio.IdFinca])
# P2: fechas mixtas
fmt = rng.random(len(sucio)) < 0.35
sucio["Fecha"] = [d.strftime("%d/%m/%Y") if m else d.strftime("%Y-%m-%d")
                  for d, m in zip(sucio.Fecha, fmt)]
# P3: litros como texto con coma, errores x10 y vacíos
lit = sucio.LitrosDia.astype(object)
coma = rng.random(len(sucio)) < 0.25
x10 = rng.random(len(sucio)) < 0.006
vacio = rng.random(len(sucio)) < 0.004
lit = [("" if v else (f"{round(l * 10):d}" if x else (str(l).replace(".", ",") if c else str(l))))
       for l, c, x, v in zip(sucio.LitrosDia, coma, x10, vacio)]
sucio["LitrosDia"] = lit
# P1: duplicados
dup = sucio.sample(frac=0.02, random_state=7)
sucio = pd.concat([sucio, dup]).sort_values("IdControl", kind="stable").reset_index(drop=True)
sucio.to_csv(out / "control_lechero.csv", index=False, sep=";", encoding="utf-8")

# P4: razas escritas de varias formas
var_raza = {"Gyr": ["Gyr", "GYR", "Gir", "gyr "], "Girolando": ["Girolando", "GIROLANDO", "Girolando "],
            "F1 Holstein x Cebú": ["F1 Holstein x Cebú", "F1 Holstein X Cebu", "f1 holstein x cebú"],
            "Simmental x Cebú": ["Simmental x Cebú", "SIMMENTAL X CEBU", "Simmental x Cebu"]}
an_out = animales.drop(columns="_mult").copy()
an_out["Raza"] = [rng.choice(var_raza[r]) if rng.random() < 0.3 else r for r in an_out.Raza]
with pd.ExcelWriter(out / "maestros_ganadera.xlsx") as xw:
    fincas.drop(columns=["_vacas", "_efecto"]).to_excel(xw, sheet_name="Fincas", index=False)
    an_out.to_excel(xw, sheet_name="Animales", index=False)
    potreros.to_excel(xw, sheet_name="Potreros", index=False)
precios.to_csv(out / "precios_leche.csv", index=False, encoding="utf-8")

print(f"control_lechero.csv: {len(sucio)} filas ({len(dup)} duplicadas), animales: {len(animales)}, "
      f"potreros: {len(potreros)}, meses: {len(precios)}")
