# Sistema de diseño — Versículo Diario

Fuente: recomendaciones de la skill `ui-ux-pro-max` (estilo "Soft UI Evolution",
paleta base de referencia "Church/Religious Organization") ajustadas a mano para
priorizar contraste y la sensación de calma pedida — sin morado saturado, con
acento dorado usado con moderación.

## Principio

Minimalista, cálido, sin distracciones. Inspirado en la moderación de Apple HIG
y la escala sistemática de Material Design 3, no en ninguno literalmente.

## Color

Definido en `apps/mobile/src/theme/colors.ts`. Claro/oscuro automático via
`useColorScheme()` (el selector manual de usuario llega en la Fase 8).

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| background | `#FBFAF7` | `#14120F` | Fondo de pantalla |
| surface | `#F5F2EA` | `#1E1B16` | Tarjetas/superficies elevadas |
| border | `#E4DFD3` | `#332F27` | Divisores |
| textPrimary | `#1F1B16` | `#F5F1E8` | Texto principal, versículo |
| textSecondary | `#4A443B` | `#C9C0AE` | Cuerpo de reflexión |
| textLabel | `#6B5A3A` | `#D4B45A` | Referencia bíblica (eyebrow) |
| accent | `#B8860B` | `#D4AF37` | Iconos activos, énfasis puntual — nunca texto de cuerpo |
| error | `#B3261E` | `#FF6B60` | Mensajes de error |

El acento dorado se eligió por su asociación tradicional con lo sagrado sin caer
en un morado/violeta saturado típico de plantillas de "iglesia" — se usa poco,
nunca como color de texto largo (falla contraste en tonos claros).

## Tipografía

- **Lora** (serif) para el texto del versículo — evoca una biblia impresa.
- **Inter** (sans) para todo lo demás — máxima legibilidad en pantallas chicas.

Escala en `apps/mobile/src/theme/typography.ts`. Cuerpo mínimo 16px (regla de
accesibilidad para móvil).

## Espaciado

Grid de 4pt: `xs=4 sm=8 md=16 lg=24 xl=32 xxl=48`. Radios: `sm=8 md=12 lg=20`.

## Iconografía

`@expo/vector-icons`, set **Feather** (trazo fino, minimal, consistente entre
iOS/Android). Sin emojis como iconos. Se empieza a usar en la Fase 5
(favoritos) — no hay iconos todavía en la pantalla principal.

## Componentes reutilizables

`apps/mobile/src/components/`:

- `Screen` — contenedor con fondo del tema + safe area.
- `AppText` — variantes tipográficas (`verse`, `title`, `body`, `label`, `caption`).
- `VerseCard` — referencia + versículo + reflexión. Se reutiliza en Favoritos/Historial (Fase 5).
- `LoadingState` / `ErrorState` — estados async consistentes entre pantallas.

`apps/mobile/src/theme/` expone `ThemeProvider` + `useTheme()`.

## Accesibilidad aplicada

- Contraste de texto verificado ≥ 4.5:1 en ambos modos.
- Objetivos táctiles ≥ 44×44 (aplica desde que existan botones, Fase 5+).
- Tipografía de cuerpo ≥ 16px.
