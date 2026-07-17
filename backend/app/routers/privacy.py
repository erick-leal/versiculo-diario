from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

_PRIVACY_HTML = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Política de Privacidad — Versículo Diario</title>
<style>
  body { font-family: system-ui, -apple-system, sans-serif; max-width: 680px; margin: 0 auto; padding: 32px 20px 80px; line-height: 1.6; color: #1F1B16; background: #FBFAF7; }
  h1 { font-size: 26px; }
  h2 { font-size: 18px; margin-top: 32px; }
  p, li { color: #4A443B; }
  a { color: #B8860B; }
</style>
</head>
<body>
<h1>Política de Privacidad — Versículo Diario</h1>
<p>Última actualización: julio de 2026</p>

<p>Versículo Diario es una aplicación gratuita para acercar a las personas a la
Biblia mediante un versículo y una reflexión diaria. Esta política explica qué
información maneja la app y por qué.</p>

<h2>Qué información recolectamos</h2>
<ul>
  <li><strong>Un identificador anónimo del dispositivo.</strong> Al abrir la
  app por primera vez, se genera un identificador aleatorio (UUID) que se
  guarda en tu celular. No está vinculado a tu nombre, email ni ninguna otra
  información personal — es solo una forma de recordar tus favoritos y
  configuración entre usos de la app.</li>
  <li><strong>Tus versículos favoritos</strong>, asociados a ese identificador
  anónimo.</li>
  <li><strong>Tu configuración de la app</strong>: preferencia de modo claro/oscuro
  y la hora que elegís para el recordatorio diario.</li>
</ul>

<h2>Qué NO recolectamos</h2>
<ul>
  <li>No pedimos ni almacenamos tu nombre, email, teléfono, ni ninguna cuenta
  personal.</li>
  <li>No accedemos a tu ubicación, contactos, fotos ni otros datos del
  dispositivo.</li>
  <li>No usamos herramientas de publicidad ni de rastreo entre apps.</li>
</ul>

<h2>Notificaciones</h2>
<p>El recordatorio diario se programa localmente en tu propio dispositivo — no
se envía desde un servidor y no requiere compartir información adicional para
funcionar.</p>

<h2>Con quién compartimos información</h2>
<p>Los datos descritos arriba se almacenan en nuestra infraestructura de backend
(Railway) únicamente para que la app funcione (guardar tus favoritos y
configuración). No vendemos ni compartimos esta información con terceros con
fines comerciales o publicitarios.</p>

<h2>Eliminar tus datos</h2>
<p>Como no manejamos cuentas, desinstalar la app elimina el identificador
anónimo de tu dispositivo. Si querés pedir la eliminación de los datos
asociados a tu identificador de todas formas, escribinos a
<a href="mailto:eleal.escobar@gmail.com">eleal.escobar@gmail.com</a>.</p>

<h2>Menores de edad</h2>
<p>La app no está dirigida específicamente a niños y no recolecta a sabiendas
información de menores de 13 años.</p>

<h2>Cambios a esta política</h2>
<p>Si esta política cambia, la fecha de "última actualización" arriba se va a
reflejar el cambio.</p>

<h2>Contacto</h2>
<p><a href="mailto:eleal.escobar@gmail.com">eleal.escobar@gmail.com</a></p>
</body>
</html>"""


@router.get("/privacy", response_class=HTMLResponse)
def privacy_policy() -> str:
    return _PRIVACY_HTML
