# -*- coding: utf-8 -*-
"""
Bot emocional diario — Telegram + GitHub Actions
Envía un consejo distinto cada día basado en un ciclo de 30 días.
"""

import os
import json
import requests
from datetime import datetime

# =========================================================
# ⚙️ CONFIGURACIÓN DE VARIABLES
# =========================================================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise SystemExit("❌ ERROR: faltan variables de entorno TELEGRAM_TOKEN o TELEGRAM_CHAT_ID.")

# =========================================================
# 📘 CARGAR BASE DE DATOS DE CONSEJOS
# =========================================================
try:
    with open("consejos.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        consejos = data.get("dias", [])
except Exception as e:
    raise SystemExit(f"❌ ERROR al leer 'consejos.json': {e}")

if not consejos:
    raise SystemExit("❌ ERROR: No hay datos en 'consejos.json'.")

# =========================================================
# 📅 SELECCIONAR CONSEJO DEL DÍA (CÍCLICO)
# =========================================================
total_dias = len(consejos)
dia_anual = datetime.now().timetuple().tm_yday
indice = (dia_anual - 1) % total_dias  # Ajuste para índice 0-based
consejo = consejos[indice]

# =========================================================
# 💬 CONSTRUIR MENSAJE
# =========================================================
mensaje = (
    f"🧠 *Consejo del día* — Día {consejo['dia']}\n"
    f"_{consejo['tema']}_\n\n"
    f"🎯 *{consejo['titulo']}*\n\n"
    f"{consejo['mensaje']}\n\n"
    f"🪶 *Acción del día:* {consejo['accion']}"
)

# =========================================================
# 🚀 ENVIAR MENSAJE A TELEGRAM
# =========================================================
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": mensaje,
    "parse_mode": "Markdown"
}

try:
    response = requests.post(url, data=payload, timeout=10)
    if response.status_code == 200:
        print("✅ Consejo enviado correctamente.")
    else:
        print(f"⚠️ Error {response.status_code}: {response.text}")
except requests.RequestException as e:
    print(f"❌ Error de conexión con Telegram: {e}")
