"""Suite de pruebas de caja negra - EnvíaYa
Estudiante: Jhonar David De Arco Mejía · Código 10182410056

Parámetros (últimos 6 dígitos 4 1 0 0 5 6):
  PMAX=50  L1=3 (incluido, D=0 par)  L2=10  RR=15%  RN=40%  V=15%  S=$2.000
  Regla E=5 impar -> recargo de fin de semana DESPUÉS de los descuentos
  Regla B=1 impar -> se aplican ambos descuentos: primero cliente, luego cupón
  Regla F=6 par   -> cupón inexistente se ignora

Todos los resultados esperados están calculados a mano (ver docs/informe.md).
Redondeo: múltiplo de $100 más cercano, $50 hacia arriba; mínimo $5.000.
"""
import pytest

from envios import calc


# ---------------------------------------------------------------- errores
@pytest.mark.parametrize(
    "id_, args",
    [
        ("CN-01", (0, "urbana", "normal", 2)),          # límite 0 (excluido)
        ("CN-02", (-1, "urbana", "normal", 2)),         # partición inválida: negativo
        ("CN-03", (50.01, "urbana", "normal", 2)),      # PMAX + epsilon
        ("CN-04", (60, "urbana", "normal", 2)),         # partición inválida: > PMAX
    ],
)
def test_peso_invalido_R1(id_, args):
    with pytest.raises(ValueError):
        calc(*args)


def test_mensaje_peso_invalido_R1():
    # R1: el mensaje debe ser exactamente "peso inválido"
    with pytest.raises(ValueError, match="peso inválido"):
        calc(0, "urbana", "normal", 2)


@pytest.mark.parametrize(
    "id_, args",
    [
        ("CN-05", (5, "insular", "normal", 2)),         # zona inválida
        ("CN-06", (5, "", "normal", 2)),                # zona vacía
        ("CN-07", (5, "urbana", "normal", 0)),          # día 0
        ("CN-08", (5, "urbana", "normal", 8)),          # día 8
    ],
)
def test_zona_o_dia_invalidos_R2(id_, args):
    with pytest.raises(ValueError):
        calc(*args)


# ------------------------------------------------- casos con resultado
CASOS = [
    # id, req, (p, z, c, d, cup), esperado, técnica
    ("CN-09", "R1/R3", (0.1, "urbana", "normal", 2, None), 6000, "VL peso mínimo válido"),
    ("CN-10", "R3", (3, "urbana", "normal", 2, None), 6000, "VL L1 incluido (D par)"),
    ("CN-11", "R3", (3.01, "urbana", "normal", 2, None), 9000, "VL L1 + epsilon"),
    ("CN-12", "R3", (10, "urbana", "normal", 2, None), 9000, "VL L2 incluido"),
    ("CN-13", "R3", (10.5, "urbana", "normal", 2, None), 9400, "VL L2 + proporcional"),
    ("CN-14", "R3", (20, "urbana", "normal", 2, None), 17000, "Partición tramo 3"),
    ("CN-15", "R1/R3", (50, "urbana", "normal", 1, None), 41000, "VL PMAX incluido"),
    ("CN-16", "R4/R8", (5, "rural", "normal", 3, None), 10400, "Partición zona rural + redondeo $50"),
    ("CN-17", "R4", (5, "nacional", "normal", 3, None), 12600, "Partición zona nacional"),
    ("CN-18", "R3/R4", (3, "rural", "normal", 3, None), 6900, "VL L1 + zona"),
    ("CN-19", "R5", (5, "urbana", "normal", 6, None), 11000, "Partición sábado"),
    ("CN-20", "R5", (5, "urbana", "normal", 7, None), 11000, "Partición domingo"),
    ("CN-21", "R5", (5, "urbana", "normal", 5, None), 9000, "VL día 5 (no finde)"),
    ("CN-22", "R6/R8", (5, "urbana", "frecuente", 2, None), 8600, "Partición cliente frecuente"),
    ("CN-23", "R6/R8", (5, "urbana", "vip", 2, None), 7700, "Partición cliente vip"),
    ("CN-24", "R6", (5, "urbana", "normal", 2, "ENVIO10"), 8100, "Partición cupón válido"),
    ("CN-25", "R6/R8", (5, "urbana", "vip", 2, "ENVIO10"), 6900, "Regla B impar: ambos (vip, luego cupón)"),
    ("CN-26", "R6/R8", (5, "urbana", "frecuente", 2, "ENVIO10"), 7700, "Regla B impar: ambos (frecuente)"),
    ("CN-27", "R7", (5, "urbana", "normal", 2, "PROMO"), 9000, "Regla F par: cupón inexistente se ignora"),
    ("CN-28", "R4/R5/R6", (4, "rural", "vip", 6, "ENVIO10"), 9900, "Regla E impar: finde después de descuentos"),
    ("CN-29", "R4/R5/R6", (4, "nacional", "vip", 7, "ENVIO10"), 11600, "Regla E impar + domingo"),
    ("CN-30", "R8", (0.5, "urbana", "vip", 2, "ENVIO10"), 5000, "Mínimo $5.000"),
    ("CN-31", "R4/R6/R8", (20, "nacional", "vip", 2, None), 20200, "Combinación peso alto + zona + vip"),
    ("CN-32", "R6/R8", (10.5, "urbana", "vip", 2, None), 8000, "Redondeo hacia arriba (7.990 -> 8.000)"),
]


@pytest.mark.parametrize(
    "id_, req, args, esperado, tecnica",
    CASOS,
    ids=[c[0] for c in CASOS],
)
def test_costo_esperado(id_, req, args, esperado, tecnica):
    assert calc(*args) == esperado


# ------------------------------- tabla de decisión: cliente x cupón x finde
# Base: peso 5 kg, urbana -> $9.000
TABLA_DECISION = [
    ("DT-01", "normal", None, 2, 9000),
    ("DT-02", "normal", None, 6, 11000),
    ("DT-03", "normal", "ENVIO10", 2, 8100),
    ("DT-04", "normal", "ENVIO10", 6, 10100),
    ("DT-05", "frecuente", None, 2, 8600),
    ("DT-06", "frecuente", None, 6, 10600),
    ("DT-07", "frecuente", "ENVIO10", 2, 7700),
    ("DT-08", "frecuente", "ENVIO10", 6, 9700),
    ("DT-09", "vip", None, 2, 7700),
    ("DT-10", "vip", None, 6, 9700),
    ("DT-11", "vip", "ENVIO10", 2, 6900),
    ("DT-12", "vip", "ENVIO10", 6, 8900),
]


@pytest.mark.parametrize(
    "id_, cliente, cupon, dia, esperado",
    TABLA_DECISION,
    ids=[t[0] for t in TABLA_DECISION],
)
def test_tabla_decision(id_, cliente, cupon, dia, esperado):
    assert calc(5, "urbana", cliente, dia, cupon) == esperado
