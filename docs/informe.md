# Parcial 3 · Ingeniería de Software I · EnvíaYa

**Universidad de La Guajira · Facultad de Ingenierías · Ingeniería de Sistemas**
**Docente:** Ing. Robert Damián Quintero Laverde · **Grupo:** B1 · **Periodo:** 2026-2 · Tercer corte
**Estudiante:** Jhonar David De Arco Mejía · **Código estudiantil:** 10182410056

## Mis parámetros

Últimos 6 dígitos: **4 1 0 0 5 6** → A=4, B=1, C=0, D=0, E=5, F=6

| A | B | C | D | E | F | PMAX | L1 | L2 | RR | RN | V | S | CAMBIO |
|---|---|---|---|---|---|------|----|----|----|----|---|---|--------|
| 4 | 1 | 0 | 0 | 5 | 6 | 50 | 3 | 10 | 15 % | 40 % | 15 % | $2.000 | 1 |

Cálculo: PMAX = 30+5·4 = 50 · L1 = 2+(1 mod 3) = 3 · L2 = 10+0 = 10 · RR = 10+5·(5 mod 4) = 15 · RN = 40+5·(6 mod 3) = 40 · V = 10+5·(4 mod 3) = 15 · S = 2000+500·(0 mod 4) = 2000 · CAMBIO = (4+6) mod 3 = 1.

Reglas por paridad:

| Dígito | Valor | Regla resultante |
|---|---|---|
| D · tramo 1 | 0 (par) | Incluye el límite: **peso ≤ 3** |
| E · recargo de fin de semana | 5 (impar) | Se suma **después** de los descuentos |
| B · cliente y cupón | 1 (impar) | Se aplican **ambos**: primero el del cliente y luego el cupón |
| F · cupón inexistente | 6 (par) | Se **ignora** |

---

## Parte 1 · Requisitos y criterios de aceptación

### 1.1 Especificación (R1–R8 con mis valores)

| ID | Regla |
|---|---|
| R1 | El peso debe cumplir 0 < peso ≤ 50. Si no, se lanza el error “peso inválido”. |
| R2 | Si la zona no es urbana, rural o nacional, o el día no está entre 1 y 7, se lanza un error. |
| R3 | Tarifa base. Tramo 1 (peso ≤ 3): $6.000. Tramo 2 (3 < peso ≤ 10): $9.000. Más de 10 kg: $9.000 + $800 por cada kg sobre 10, proporcional. |
| R4 | Recargo por zona. Rural: +15 %. Nacional: +40 %. Urbana: sin recargo. |
| R5 | Fin de semana (6 = sábado y 7 = domingo): +$2.000, **después** de los descuentos. |
| R6 | Descuento de cliente: frecuente 5 %, VIP 15 %. Cupón ENVIO10: 10 %. Si hay cliente y cupón se aplican ambos: primero el del cliente y luego el cupón. |
| R7 | Un cupón que no existe se ignora. |
| R8 | El costo nunca es menor que $5.000. Se redondea al múltiplo de $100 más cercano; los $50 redondean hacia arriba. |

Orden de cálculo: base → zona → descuento de cliente → cupón → fin de semana → mínimo $5.000 → redondeo.

### 1.2 Historias de usuario

**HU-01 · Validar el envío (R1, R2)**
Como operador de EnvíaYa quiero que el sistema rechace envíos con datos inválidos para no cotizar paquetes imposibles.
- *CA-1.* **Dado** un peso de 0, negativo o mayor que 50 kg, **cuando** calculo el costo, **entonces** se lanza el error “peso inválido”.
- *CA-2.* **Dado** una zona distinta de urbana, rural o nacional, **cuando** calculo el costo, **entonces** se lanza un error.
- *CA-3.* **Dado** un día menor que 1 o mayor que 7, **cuando** calculo el costo, **entonces** se lanza un error.

**HU-02 · Calcular tarifa, zona y fin de semana (R3, R4, R5)**
Como cliente quiero que el costo dependa del peso, la zona y el día para pagar un precio justo.
- *CA-1.* **Dado** un peso de 3 kg, **cuando** calculo el costo base, **entonces** aplica el tramo 1 ($6.000) porque el límite está incluido.
- *CA-2.* **Dado** un envío rural o nacional, **cuando** calculo, **entonces** se suma 15 % o 40 % sobre la tarifa base.
- *CA-3.* **Dado** un envío en sábado o domingo, **cuando** calculo, **entonces** se suman $2.000 después de aplicar los descuentos.

**HU-03 · Descuentos, mínimo y redondeo (R6, R7, R8)**
Como cliente frecuente o VIP quiero que mis descuentos y cupones se apliquen para pagar menos.
- *CA-1.* **Dado** un cliente VIP con cupón ENVIO10, **cuando** calculo, **entonces** se aplica 15 % y luego 10 % sobre el resultado.
- *CA-2.* **Dado** un cupón que no existe, **cuando** calculo, **entonces** se ignora y el cálculo continúa sin error.
- *CA-3.* **Dado** un costo calculado menor que $5.000, **cuando** calculo, **entonces** el resultado es $5.000; y si queda en $x50, **entonces** se redondea hacia arriba al siguiente $100.

### 1.3 Matriz de trazabilidad (se completa en las partes siguientes)

| Requisito | Historia | Casos de prueba | Código (líneas heredadas) |
|---|---|---|---|
| R1 | HU-01 | CN-01…04, CN-09, CN-15, test_mensaje | 13–14 |
| R2 | HU-01 | CN-05…08 | no existe (DEF-01, DEF-02) |
| R3 | HU-02 | CN-09…15, CN-18 | 15–20 |
| R4 | HU-02 | CN-16, 17, 18, 31 | 21–26 |
| R5 | HU-02, HU-03 | CN-19, 20, 21, 28, 29, DT-02/04/06/08/10/12 | 27–29 |
| R6 | HU-03 | CN-22…26, DT-05…12 | 30–36 |
| R7 | HU-03 | CN-27 | 34–36 |
| R8 | HU-03 | CN-16, 22, 23, 30, 32 | 37–41 |

---

## Parte 2 · Plan de pruebas

**Alcance.** Se prueba la función `calc` (R1–R8). Fuera de alcance: interfaz de usuario, base de datos, concurrencia, rendimiento.

**Niveles de prueba aplicados al caso**

| Nivel | Cómo se aplica a EnvíaYa |
|---|---|
| Unidad | Cada rama de `calc` y, tras refactorizar, cada función extraída (tarifa, zona, descuentos, redondeo) con pytest. |
| Integración | Verifica que las funciones extraídas / estrategias trabajan juntas en el orden correcto (base → zona → descuentos → finde → mínimo → redondeo). |
| Sistema | Se invoca `calc` como lo haría el sistema de envíos, con entradas completas de extremo a extremo (matriz de 45 casos). |
| Aceptación | Los criterios Dado/Cuando/Entonces de HU-01 a HU-03 se verifican con casos de la matriz. La empresa los aprobaría contra su regla de negocio. |

**Estrategia.** Caja negra (particiones, valores límite, tabla de decisión) + caja blanca (cobertura de sentencias y ramas, caminos independientes). Resultados esperados calculados a mano, no con el código. Pruebas de regresión tras cada corrección.

**Ambiente.** Python 3.13, pytest, pytest-cov, Git/GitHub. Ejecución local.

**Roles.** Analista de calidad (diseña casos), desarrollador de mantenimiento (corrige y refactoriza), líder de configuración (ramas, etiquetas, CHANGELOG). En este parcial los tres los ejerzo yo.

**Riesgos y mitigación**

| Riesgo | Mitigación |
|---|---|
| Errores de coma flotante en dinero (ej. 0,05·t) | Casos con valores terminados en $50 y pruebas de redondeo; en la refactorización usar `Decimal` o enteros. |
| Interpretar mal las reglas por paridad | Parámetros y reglas documentados al inicio; casos que distinguen cada regla (DT-01…12). |
| Que la refactorización cambie el comportamiento | Suite de regresión completa antes y después. |
| Resultados esperados mal calculados | Cálculo a mano documentado y contrastado con una implementación de referencia independiente. |

**Criterios de entrada:** especificación aprobada, CONFIG correcto, código heredado etiquetado v1.0.0, ambiente instalado.
**Criterios de salida:** 100 % de los casos ejecutados; 100 % pasando tras correcciones; cobertura de sentencias y ramas ≥ 95 %; cero defectos críticos/altos abiertos.

---

## Parte 3 · Diseño de casos de caja negra

### 3.1 Particiones de equivalencia

| Entrada | Válidas | Inválidas |
|---|---|---|
| peso | (0, 3], (3, 10], (10, 50] | ≤ 0, > 50 |
| zona | urbana, rural, nacional | cualquier otra, vacía |
| cliente | normal, frecuente, vip | (no definido en la especificación) |
| día | 1–5 (entre semana), 6, 7 | < 1, > 7 |
| cupón | ninguno, ENVIO10 | cupón inexistente → se **ignora** (F par); no es error |

### 3.2 Valores límite del peso (L1 = 3 incluido)

| Frontera | Valores | Resultado esperado |
|---|---|---|
| 0 | 0 · 0,1 | error · $6.000 |
| L1 = 3 | 3 · 3,01 | $6.000 (incluido) · $9.000 |
| L2 = 10 | 10 · 10,5 | $9.000 · $9.400 |
| PMAX = 50 | 50 · 50,01 | $41.000 · error |

### 3.3 Tabla de decisión: cliente × cupón × fin de semana (B impar, E impar)

Base: 5 kg, urbana = $9.000. Fin de semana +$2.000 **después** de los descuentos.

| Regla | Cliente | Cupón | Fin de semana | Cálculo | Esperado |
|---|---|---|---|---|---|
| DT-01 | normal | no | no | 9.000 | $9.000 |
| DT-02 | normal | no | sí | 9.000 + 2.000 = 11.000 | $11.000 |
| DT-03 | normal | sí | no | 9.000 × 0,90 = 8.100 | $8.100 |
| DT-04 | normal | sí | sí | 8.100 + 2.000 = 10.100 | $10.100 |
| DT-05 | frecuente | no | no | 9.000 × 0,95 = 8.550 | $8.600 |
| DT-06 | frecuente | no | sí | 8.550 + 2.000 = 10.550 | $10.600 |
| DT-07 | frecuente | sí | no | 8.550 × 0,90 = 7.695 | $7.700 |
| DT-08 | frecuente | sí | sí | 7.695 + 2.000 = 9.695 | $9.700 |
| DT-09 | vip | no | no | 9.000 × 0,85 = 7.650 | $7.700 |
| DT-10 | vip | no | sí | 7.650 + 2.000 = 9.650 | $9.700 |
| DT-11 | vip | sí | no | 7.650 × 0,90 = 6.885 | $6.900 |
| DT-12 | vip | sí | sí | 6.885 + 2.000 = 8.885 | $8.900 |

### 3.4 Matriz de casos de prueba (45 en total; implementados en `tests/test_envios.py`)

| ID | Req. | Entradas (peso, zona, cliente, día, cupón) | Esperado | Técnica |
|---|---|---|---|---|
| CN-01 | R1 | 0, urbana, normal, 2 | error | Valor límite (0) |
| CN-02 | R1 | −1, urbana, normal, 2 | error | Partición inválida |
| CN-03 | R1 | 50,01, urbana, normal, 2 | error | Valor límite (PMAX+) |
| CN-04 | R1 | 60, urbana, normal, 2 | error | Partición inválida |
| CN-05 | R2 | 5, insular, normal, 2 | error | Partición inválida (zona) |
| CN-06 | R2 | 5, "", normal, 2 | error | Partición inválida (zona vacía) |
| CN-07 | R2 | 5, urbana, normal, 0 | error | Valor límite (día 0) |
| CN-08 | R2 | 5, urbana, normal, 8 | error | Valor límite (día 8) |
| CN-09 | R1/R3 | 0,1, urbana, normal, 2 | $6.000 | Valor límite |
| CN-10 | R3 | 3, urbana, normal, 2 | $6.000 | Límite L1 incluido |
| CN-11 | R3 | 3,01, urbana, normal, 2 | $9.000 | Límite L1+ |
| CN-12 | R3 | 10, urbana, normal, 2 | $9.000 | Límite L2 incluido |
| CN-13 | R3 | 10,5, urbana, normal, 2 | $9.400 | Límite L2+ |
| CN-14 | R3 | 20, urbana, normal, 2 | $17.000 | Partición tramo 3 |
| CN-15 | R1/R3 | 50, urbana, normal, 1 | $41.000 | Límite PMAX |
| CN-16 | R4/R8 | 5, rural, normal, 3 | $10.400 | Partición zona + redondeo |
| CN-17 | R4 | 5, nacional, normal, 3 | $12.600 | Partición zona |
| CN-18 | R3/R4 | 3, rural, normal, 3 | $6.900 | Límite + zona |
| CN-19 | R5 | 5, urbana, normal, 6 | $11.000 | Partición sábado |
| CN-20 | R5 | 5, urbana, normal, 7 | $11.000 | Partición domingo |
| CN-21 | R5 | 5, urbana, normal, 5 | $9.000 | Límite (viernes) |
| CN-22 | R6/R8 | 5, urbana, frecuente, 2 | $8.600 | Partición cliente |
| CN-23 | R6/R8 | 5, urbana, vip, 2 | $7.700 | Partición cliente |
| CN-24 | R6 | 5, urbana, normal, 2, ENVIO10 | $8.100 | Partición cupón |
| CN-25 | R6/R8 | 5, urbana, vip, 2, ENVIO10 | $6.900 | Regla B (ambos) |
| CN-26 | R6/R8 | 5, urbana, frecuente, 2, ENVIO10 | $7.700 | Regla B (ambos) |
| CN-27 | R7 | 5, urbana, normal, 2, PROMO | $9.000 | Regla F (ignorar) |
| CN-28 | R4/R5/R6 | 4, rural, vip, 6, ENVIO10 | $9.900 | Regla E (después) |
| CN-29 | R4/R5/R6 | 4, nacional, vip, 7, ENVIO10 | $11.600 | Regla E (después) |
| CN-30 | R8 | 0,5, urbana, vip, 2, ENVIO10 | $5.000 | Mínimo |
| CN-31 | R4/R6/R8 | 20, nacional, vip, 2 | $20.200 | Combinación |
| CN-32 | R6/R8 | 10,5, urbana, vip, 2 | $8.000 | Redondeo hacia arriba |
| DT-01…12 | R5/R6 | ver 3.3 | ver 3.3 | Tabla de decisión |
| MSG | R1 | 0, urbana, normal, 2 | mensaje “peso inválido” | Verificación del mensaje |

### 3.5 Cálculo paso a paso (7 casos)

**CN-16** (5 kg, rural, normal, día 3) — 1) 5 kg ∈ (3, 10] → $9.000. 2) Rural +15 %: 9.000 × 1,15 = $10.350. 3) Día 3, sin fin de semana. 4) Cliente normal, sin cupón. 5) ≥ $5.000. 6) $50 sube → **$10.400**.

**CN-25** (5 kg, urbana, vip, día 2, ENVIO10) — 1) $9.000. 2) Urbana: sin recargo. 3) B impar, ambos: VIP 15 % → 9.000 × 0,85 = $7.650. 4) Cupón 10 % → 7.650 × 0,90 = $6.885. 5) Redondeo → **$6.900**.

**CN-28** (4 kg, rural, vip, sábado, ENVIO10) — 1) 4 kg > 3 → $9.000. 2) Rural: 9.000 × 1,15 = $10.350. 3) VIP: 10.350 × 0,85 = $8.797,50. 4) Cupón: 8.797,50 × 0,90 = $7.917,75. 5) Sábado y E impar: el recargo va **después** → 7.917,75 + 2.000 = $9.917,75. 6) Redondeo → **$9.900**.

**CN-29** (4 kg, nacional, vip, domingo, ENVIO10) — 1) $9.000. 2) Nacional: 9.000 × 1,40 = $12.600. 3) VIP: 12.600 × 0,85 = $10.710. 4) Cupón: 10.710 × 0,90 = $9.639. 5) Domingo, después: 9.639 + 2.000 = $11.639. 6) Redondeo → **$11.600**.

**CN-30** (0,5 kg, urbana, vip, día 2, ENVIO10) — 1) Tramo 1 → $6.000. 2) VIP: 5.100. 3) Cupón: 4.590. 4) 4.590 < 5.000 → mínimo **$5.000**.

**CN-31** (20 kg, nacional, vip, día 2) — 1) 9.000 + (20 − 10) × 800 = $17.000. 2) Nacional: 17.000 × 1,40 = $23.800. 3) VIP: 23.800 × 0,85 = $20.230. 4) Redondeo → **$20.200**.

**CN-32** (10,5 kg, urbana, vip, día 2) — 1) 9.000 + 0,5 × 800 = $9.400. 2) VIP: 9.400 × 0,85 = $7.990. 3) Redondeo al $100 más cercano → **$8.000**.

---

## Parte 4 · Caja blanca

### 4.1 Grafo de flujo de `calc`

> **Pendiente (hazlo tú):** dibuja el grafo de flujo de `calc` (a mano o con draw.io) numerando los nodos con las líneas de `src/envios.py` y pégalo aquí como imagen. Nodos predicado: líneas 13 (dos condiciones: `p <= 0`, `p > 50`), 15, 17, 21, 23, 25, 28, 30, 32, 34, 35, 37 y 39.

### 4.2 Complejidad ciclomática (verifica con tu dibujo)

- **Nodos predicado:** 14 condiciones (la línea 13 cuenta 2 por el `or`) → V(G) = 14 + 1 = **15**. Si cuentas la línea 13 como una sola decisión: 13 + 1 = 14.
- **Aristas y nodos:** V(G) = E − N + 2. Con tu grafo debe dar el mismo valor (15).
- **Regiones:** número de regiones cerradas + la exterior = 15.

### 4.3 Caminos independientes y cobertura

> **Pendiente:** lista 15 caminos independientes y asigna a cada uno un caso de la matriz (por ejemplo: peso inválido → CN-01/CN-03; tramo 1 → CN-10; tramo 2 → CN-12; tramo 3 → CN-14; urbana → CN-10; rural → CN-16; nacional → CN-17; fin de semana → CN-19; frecuente → CN-22; vip → CN-23; cupón válido → CN-24; cupón inexistente → CN-27; mínimo → CN-30; `flag` verdadero → requiere un caso extra con `flag=True`).

Cobertura medida contra el código heredado con la suite actual: **sentencias 28/29 = 96 %**, la línea 40 (`print` bajo `flag`) no se ejecuta; ramas: 1 rama parcial (la de `flag`). Para el 100 % basta un caso con `flag=True` (esa rama desaparece al eliminar `flag` en la Parte 6).

---

## Parte 5 · Automatización, ejecución y defectos

### 5.1 y 5.2 Ejecución y cobertura

```bash
pytest -v
pytest --cov=envios --cov-branch --cov-report=term-missing
```

> **Pendiente:** adjunta capturas de pantalla de estos comandos (fallando contra v1.0.0 y pasando tras corregir).

Resultado contra el código heredado: **45 casos, 21 pasan, 24 fallan**.

### 5.3 Reporte de defectos (preliminar; confirma cada uno ejecutando)

| ID | Título | Req. | Pasos | Esperado | Obtenido | Severidad / Prioridad |
|---|---|---|---|---|---|---|
| DEF-01 | No valida la zona | R2 | `calc(5, "insular", "normal", 2)` | Error | $9.000 (sin error; ignora la zona) | Alta / Alta: cotiza cualquier zona inexistente sin recargo |
| DEF-02 | No valida el día | R2 | `calc(5, "urbana", "normal", 0)` o con día 8 | Error | Calcula (día 8 incluso cobra fin de semana) | Media / Media: dato de entrada incorrecto que hoy produce un cobro |
| DEF-03 | El sábado no cobra fin de semana | R5 | `calc(5, "urbana", "normal", 6)` | $11.000 | $9.000 | Alta / Alta: pérdida de ingresos todos los sábados (`d > 6` en lugar de `d >= 6`) |
| DEF-04 | Recargo de fin de semana antes de los descuentos | R5/R6 (regla E impar) | `calc(4, "nacional", "vip", 7, "ENVIO10")` | $11.600 | $11.100 | Alta / Alta: el recargo queda descontado; cada domingo cobra de menos |
| DEF-05 | Redondeo por truncamiento | R8 | `calc(10.5, "urbana", "vip", 2)` | $8.000 | $7.900 | Media / Media: diferencia de hasta $99 en casi todos los envíos |
| DEF-06 | Mensaje de error sin tilde | R1 | `calc(0, "urbana", "normal", 2)` | “peso inválido” | “peso invalido” | Baja / Baja: cosmético, no altera el costo |

**Líneas del código heredado que NO son defecto con mi especificación** (úsalas en la sustentación): línea 13 (`p > 50` coincide con PMAX = 50 aunque es número mágico), línea 15 (`<=` coincide con D par), líneas 30–36 (aplicar ambos descuentos coincide con B impar), línea 34–36 (ignorar cupón inexistente coincide con F par).

### 5.4 Métricas (código heredado)

| Métrica | Valor |
|---|---|
| Casos que pasan | 21 / 45 = 46,7 % |
| Defectos por severidad | Alta: 3 · Media: 2 · Baja: 1 |
| Densidad de defectos | 6 defectos / 41 líneas × 100 = 14,6 por cada 100 líneas |
| Cobertura de sentencias | 96 % (28/29) |
| Cobertura de ramas | 25/26 ramas (solo falta la de `flag`) |

---

## Parte 6 · Mantenimiento y refactorización

### 6.1 Malos olores (líneas del código heredado)

| # | Mal olor | Línea(s) | Deuda técnica que genera |
|---|---|---|---|
| 1 | Números mágicos (6000, 9000, 800, 0,05, 0,10, 5000, 50, 100) | 13, 16, 18, 20, 31, 36, 37–38, 41 | Cambiar una tarifa exige buscarla en el código; riesgo de olvidar un lugar |
| 2 | Argumento bandera (*flag argument*) | 12, 39–40 | Una función con dos comportamientos; interfaz confusa y rama extra por probar |
| 3 | Función larga / hace de todo (*long method*) | 12–41 | Validación, tarifa, zona, descuentos y redondeo mezclados; difícil de probar por separado |
| 4 | Asignación sin efecto (*dead code*) `t = t` | 22 | Ruido que confunde al lector |
| 5 | Condicionales repetidos sobre tipo (switch en cadena) | 21–26, 30–36 | Agregar zona o cliente obliga a editar `calc`; viola abierto/cerrado → patrón Estrategia |
| 6 | Nombres poco descriptivos (`p, z, c, d, cup, t`) | 12 | Código ilegible; errores de interpretación |
| 7 | Efecto secundario / E/S dentro del cálculo (`print`) | 40 | Función de negocio acoplada a la consola |
| 8 | Comparación `!= None` y `if` anidados innecesarios | 34–35 | Estilo no idiomático; complejidad innecesaria |
| 9 | Dinero con punto flotante | 24, 26, 31, 33, 36, 41 | Errores de redondeo; ya causó DEF-05 |
| 10 | Obsesión por primitivos (zona/cliente como strings) | 21–33 | Errores de tipeo silenciosos (origen de DEF-01) |

### 6.2 Clasificación de los cambios

| Cambio | Tipo de mantenimiento |
|---|---|
| Corregir DEF-01…DEF-06 | Correctivo |
| Extraer funciones, constantes con nombre, mejores nombres | Perfectivo |
| Eliminar `flag`, patrón Estrategia, usar `Decimal` | Preventivo |
| Adaptar a cambios de negocio/entorno (Parte 8) | Perfectivo (nueva funcionalidad pedida por el negocio) |

### 6.3–6.6 Refactorización, regresión y comparación

> **Pendiente (rama `refactor/estrategia`):** extraer funciones, constantes con nombre, eliminar `flag`, aplicar Estrategia (zonas o descuentos) con diagrama de clases UML, corregir DEF-01…06 en sus ramas `fix/DEF-0x`, re-ejecutar la suite (45/45 en verde) y completar:

| Métrica | Antes (v1.0.0) | Después |
|---|---|---|
| Complejidad ciclomática de `calc` | 15 | |
| Líneas | 41 | |
| Cobertura sentencias / ramas | 96 % / 96 % | |

---

## Parte 7 · Gestión de configuración

> **Pendiente (haz los commits a lo largo del día, no todos juntos):**
> 1. `git tag v1.0.0` sobre el código heredado.
> 2. Ramas `test/suite`, `fix/DEF-01` … `fix/DEF-06`, `refactor/estrategia`; integrar con merge o PR.
> 3. Versión: quitar `flag` cambia la interfaz pública → cambio incompatible → **MAJOR (2.0.0)**; solo las correcciones serían 1.0.1; el cambio de la Parte 8 agrega funcionalidad compatible → **MINOR (2.1.0)**.
> 4. Completar `CHANGELOG.md` (Keep a Changelog) y notas de la versión.
> 5. Adjuntar la salida de `git log --oneline --graph --all`.

---

## Parte 8 · Solicitud de cambio (A + F) mod 3 = (4 + 6) mod 3 = **1**

> *Nuevo tipo de cliente **empresarial** con un 12 % de descuento. Si el peso es mayor que L2 (10 kg), el recargo de zona no se cobra.*

### 8.1 Análisis de impacto

| Elemento | Afectado |
|---|---|
| Requisitos | R3/R4 (el recargo de zona depende del peso y del cliente), R6 (nuevo descuento 12 %), R8 (redondeo del nuevo resultado) |
| Historias | HU-02 (CA-2 zona), HU-03 (descuentos) |
| Casos existentes a revisar | CN-14, CN-15, CN-17, CN-31 (peso > 10 con zona), CN-22…26, DT-05…12 |
| Código | Líneas 21–26 (zona) y 30–36 (descuentos) del heredado; en la versión refactorizada, la estrategia de zona y la de descuento de cliente |

**Ambigüedad a aclarar con el docente:** ¿la exención del recargo de zona con peso > 10 kg aplica solo al cliente empresarial o a todos? Documenta tu supuesto; el análisis anterior lo considera para el cliente empresarial.

### 8.2 Tipo de mantenimiento

Perfectivo (se agrega funcionalidad nueva solicitada por el negocio).

### 8.3 Casos de prueba nuevos (escribir primero, ver fallar)

| ID | Entradas | Cálculo | Esperado |
|---|---|---|---|
| CR-01 | 5 kg, urbana, empresarial, día 2 | 9.000 × 0,88 = 7.920 | $7.900 |
| CR-02 | 12 kg, rural, empresarial, día 2 | 9.000 + 2 × 800 = 10.600; sin recargo de zona; × 0,88 = 9.328 | $9.300 |
| CR-03 | 10 kg, rural, empresarial, día 2 | 10 no es mayor que L2 → rural cobra: 9.000 × 1,15 = 10.350; × 0,88 = 9.108 | $9.100 |
| CR-04 | 5 kg, urbana, empresarial, día 2, ENVIO10 | B impar: 9.000 × 0,88 = 7.920; × 0,90 = 7.128 | $7.100 |

### 8.4 Implementación y versión

> **Pendiente:** rama `feature/cliente-empresarial`, pruebas primero, implementación, versión 2.1.0 y actualización del CHANGELOG.

---

## Preparación para la sustentación

Practica el ciclo de 20 minutos: **(1)** escribir la prueba que reproduce el defecto y verla fallar, **(2)** corregir, **(3)** correr toda la regresión, **(4)** commit y etiqueta con la versión correcta. Debes poder explicar por qué cada regla de paridad te da el comportamiento que tienes.
