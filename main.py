# --- Consejos cíclicos por día ---
from datetime import datetime

with open("consejos.json", "r", encoding="utf-8") as f:
    data = json.load(f)

dia_actual = datetime.now().timetuple().tm_yday % len(data["dias"])
consejo = data["dias"][dia_actual - 1]

mensaje = (
    f"🧠 *Consejo del día* — Día {consejo['dia']}\n"
    f"_{consejo['tema']}_\n\n"
    f"🎯 *{consejo['titulo']}*\n\n"
    f"{consejo['mensaje']}\n\n"
    f"🪶 *Acción del día:* {consejo['accion']}"
)
