# Parcial 3 · Ingeniería de Software I · EnvíaYa

**Estudiante:** Jhonar David De Arco Mejía · **Código:** 10182410056
**Universidad de La Guajira** · Ingeniería de Sistemas · Grupo B1 · 2026-2

## Estructura

```
src/envios.py          código heredado v1.0.0 (CONFIG ya llenado)
tests/test_envios.py   suite pytest (45 casos, resultados esperados calculados a mano)
docs/informe.md        base del informe (Partes 1 a 8)
CHANGELOG.md           formato Keep a Changelog
```

## Uso

```bash
python -m venv .venv && source .venv/bin/activate    # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v                                            # ejecutar pruebas
pytest --cov=envios --cov-branch --cov-report=term-missing   # cobertura sentencias + ramas
```

## Flujo de git sugerido (haz los commits mientras trabajas, no al final)

```bash
git init && git add . && git commit -m "chore: código heredado v1.0.0"
git tag v1.0.0
git switch -c test/suite        # ... commits ... luego merge a main
git switch -c fix/DEF-01        # una rama por defecto
git switch -c refactor/estrategia
git log --oneline --graph --all # salida para el informe
```
