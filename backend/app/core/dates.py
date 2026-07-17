from datetime import date, datetime
from zoneinfo import ZoneInfo

# La mayoria de la audiencia esperada esta en America Latina. Un corte fijo
# en esta zona evita que el "dia" cambie horas antes de la medianoche real
# del usuario (lo que pasaba con UTC puro, ver CLAUDE.md).
APP_TIMEZONE = ZoneInfo("America/Bogota")


def today() -> date:
    return datetime.now(APP_TIMEZONE).date()
