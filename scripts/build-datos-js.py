#!/usr/bin/env python3
"""Convierte data/sso.json a src/data/datos.js. Genérico — detecta silos automáticamente."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, 'data', 'sso.json')
JS_PATH = os.path.join(ROOT, 'src', 'data', 'datos.js')

with open(JSON_PATH, encoding='utf-8') as f:
    data = json.load(f)

js = "// AUTO-GENERATED desde data/sso.json. NO EDITAR A MANO.\n\n"

# Site config (siempre presente)
js += f"export const site = {json.dumps(data['site'], ensure_ascii=False, indent=2)};\n\n"

# Detectar silos: cada key que sea lista de objetos con 'slug'
silos = []
for key, val in data.items():
    if key == 'site':
        continue
    if isinstance(val, list) and val and isinstance(val[0], dict) and 'slug' in val[0]:
        js += f"export const {key} = {json.dumps(val, ensure_ascii=False, indent=2)};\n\n"
        silos.append(key)
    elif isinstance(val, dict):
        # Campos object (ej home_content)
        js += f"export const {key} = {json.dumps(val, ensure_ascii=False, indent=2)};\n\n"

# Combinar todos los silos (los que tienen pages indexables, excluyendo institucionales si existen)
indexable = [s for s in silos if s != 'institutional']
inst = [s for s in silos if s == 'institutional']

js += f"// allPages: indexable (sin institucionales)\n"
js += f"export const allPages = [{', '.join(f'...{s}' for s in indexable)}];\n"
if inst:
    js += f"export const allPagesWithInst = [{', '.join(f'...{s}' for s in silos)}];\n"
else:
    js += f"export const allPagesWithInst = allPages;\n"

os.makedirs(os.path.dirname(JS_PATH), exist_ok=True)
with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

print(f"OK: datos.js generado ({os.path.getsize(JS_PATH):,} bytes)")
print(f"  Silos detectados: {silos}")
print(f"  Indexables: {indexable}")
