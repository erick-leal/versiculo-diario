"""Siembra un lote de 30 dias de versiculos (RVA1909, dominio publico) y
reflexiones. Las reflexiones quedan en status="ai_generated" (no
"published") a proposito: el flujo del proyecto exige revision humana
antes de publicar. Revisarlas y publicarlas desde el panel admin
(/reflections) antes de que llegue cada fecha, o el endpoint /daily-verse
va a devolver 404 para esos dias (filtra por status="published").

El texto de los versiculos viene del dump SQL de la RVA1909 publicado en
github.com/iglesianazaret/biblia-reina-valera-1909-base-datos-sql
(dominio publico), no escrito de memoria.
"""

import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.database import SessionLocal
from app.models import DailyVerse, Favorite, Reflection, Verse

# (book, chapter, verse_start, verse_end, reference, text)
VERSES = [
    ("Juan", 3, 16, None, "Juan 3:16",
     "Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito, "
     "para que todo aquel que en Él cree, no se pierda, mas tenga vida eterna."),
    ("Salmos", 23, 1, None, "Salmos 23:1",
     "Jehová es mi pastor; nada me faltará."),
    ("Filipenses", 4, 13, None, "Filipenses 4:13",
     "Todo lo puedo en Cristo que me fortalece."),
    ("Salmos", 46, 1, None, "Salmos 46:1",
     "Dios es nuestro amparo y fortaleza, Nuestro pronto auxilio en las tribulaciones."),
    ("Isaías", 41, 10, None, "Isaías 41:10",
     "No temas, que yo soy contigo; no desmayes, que yo soy tu Dios que te esfuerzo: "
     "siempre te ayudaré, siempre te sustentaré con la diestra de mi justicia."),
    ("Jeremías", 29, 11, None, "Jeremías 29:11",
     "Porque yo sé los pensamientos que tengo acerca de vosotros, dice Jehová, "
     "pensamientos de paz, y no de mal, para daros el fin que esperáis."),
    ("Romanos", 8, 28, None, "Romanos 8:28",
     "Y sabemos que a los que a Dios aman, todas las cosas les ayudan a bien, "
     "es a saber, a los que conforme al propósito son llamados."),
    ("Proverbios", 3, 5, 6, "Proverbios 3:5-6",
     "Fíate de Jehová de todo tu corazón, Y no estribes en tu prudencia. "
     "Reconócelo en todos tus caminos, Y él enderezará tus veredas."),
    ("Mateo", 11, 28, None, "Mateo 11:28",
     "Venid a mí todos los que estáis trabajados y cargados, que yo os haré descansar."),
    ("1 Corintios", 13, 4, 7, "1 Corintios 13:4-7",
     "La caridad es sufrida, es benigna; la caridad no tiene envidia, la caridad no "
     "hace sinrazón, no se ensancha; No es injuriosa, no busca lo suyo, no se irrita, "
     "no piensa el mal; No se huelga de la injusticia, mas se huelga de la verdad; "
     "Todo lo sufre, todo lo cree, todo lo espera, todo lo soporta."),
    ("Salmos", 118, 24, None, "Salmos 118:24",
     "Este es el día que hizo Jehová Nos gozaremos y alegraremos en él."),
    ("Josué", 1, 9, None, "Josué 1:9",
     "Mira que te mando que te esfuerces y seas valiente: no temas ni desmayes, "
     "porque Jehová tu Dios será contigo en donde quiera que fueres."),
    ("Filipenses", 4, 6, 7, "Filipenses 4:6-7",
     "Por nada estéis afanosos; sino sean notorias vuestras peticiones delante de "
     "Dios en toda oración y ruego, con hacimiento de gracias. Y la paz de Dios, que "
     "sobrepuja todo entendimiento, guardará vuestros corazones y vuestros "
     "entendimientos en Cristo Jesús."),
    ("2 Corintios", 5, 17, None, "2 Corintios 5:17",
     "De modo que si alguno está en Cristo, nueva criatura es: las cosas viejas "
     "pasaron; he aquí todas son hechas nuevas."),
    ("Salmos", 34, 18, None, "Salmos 34:18",
     "Cercano está Jehová a los quebrantados de corazón; Y salvará a los contritos "
     "de espíritu."),
    ("Mateo", 6, 33, None, "Mateo 6:33",
     "Mas buscad primeramente el reino de Dios y su justicia, y todas estas cosas "
     "os serán añadidas."),
    ("Romanos", 12, 2, None, "Romanos 12:2",
     "Y no os conforméis a este siglo; mas reformaos por la renovación de vuestro "
     "entendimiento, para que experimentéis cuál sea la buena voluntad de Dios, "
     "agradable y perfecta."),
    ("Gálatas", 5, 22, 23, "Gálatas 5:22-23",
     "Mas el fruto del Espíritu es: caridad, gozo, paz, tolerancia, benignidad, "
     "bondad, fe, Mansedumbre, templanza: contra tales cosas no hay ley."),
    ("Salmos", 27, 1, None, "Salmos 27:1",
     "Jehová es mi luz y mi salvación: ¿de quién temeré? Jehová es la fortaleza de "
     "mi vida: ¿de quién he de atemorizarme?"),
    ("Isaías", 40, 31, None, "Isaías 40:31",
     "Mas los que esperan a Jehová tendrán nuevas fuerzas; levantarán las alas como "
     "águilas, correrán, y no se cansarán, caminarán, y no se fatigarán."),
    ("1 Pedro", 5, 7, None, "1 Pedro 5:7",
     "Echando toda vuestra solicitud en Él, porque Él tiene cuidado de vosotros."),
    ("Salmos", 91, 1, 2, "Salmos 91:1-2",
     "El que habita al abrigo del Altísimo, Morará bajo la sombra del Omnipotente. "
     "Diré yo a Jehová: Esperanza mía, y castillo mío; Mi Dios, en él confiaré."),
    ("Mateo", 5, 14, 16, "Mateo 5:14-16",
     "Vosotros sois la luz del mundo: una ciudad asentada sobre un monte no se "
     "puede esconder. Ni se enciende una lámpara y se pone debajo de un almud, mas "
     "sobre el candelero, y alumbra a todos los que están en casa. Así alumbre "
     "vuestra luz delante de los hombres, para que vean vuestras obras buenas, y "
     "glorifiquen a vuestro Padre que está en los cielos."),
    ("Efesios", 2, 8, 9, "Efesios 2:8-9",
     "Porque por gracia sois salvos por la fe; y esto no de vosotros, pues es don "
     "de Dios: No por obras, para que nadie se gloríe."),
    ("Salmos", 139, 14, None, "Salmos 139:14",
     "Te alabaré; porque formidables, maravillosas son tus obras: Estoy "
     "maravillado, Y mi alma lo conoce mucho."),
    ("Lamentaciones", 3, 22, 23, "Lamentaciones 3:22-23",
     "Es por la misericordia de Jehová que no somos consumidos, porque nunca "
     "decayeron sus misericordias. Nuevas son cada mañana; grande es tu fidelidad."),
    ("Hebreos", 11, 1, None, "Hebreos 11:1",
     "Es pues la fe la sustancia de las cosas que se esperan, la demostración de "
     "las cosas que no se ven."),
    ("Juan", 14, 27, None, "Juan 14:27",
     "La paz os dejo, mi paz os doy: no como el mundo la da, yo os la doy. No se "
     "turbe vuestro corazón, ni tenga miedo."),
    ("Salmos", 121, 1, 2, "Salmos 121:1-2",
     "Alzaré mis ojos a los montes, De donde vendrá mi socorro. Mi socorro viene "
     "de Jehová, Que hizo los cielos y la tierra."),
    ("1 Juan", 4, 19, None, "1 Juan 4:19",
     "Nosotros le amamos a Él, porque Él nos amó primero."),
]

# reference -> (title, body). Juan 3:16 no esta aca: ya tiene reflexion publicada.
REFLECTIONS = {
    "Salmos 23:1": (
        "Lo que significa que no te falte nada",
        "Decir «nada me faltará» no es una promesa de que la vida será fácil — David "
        "escribió este salmo en medio de peligros reales, no en la comodidad. Es una "
        "declaración de confianza: si Dios es quien guía, lo esencial siempre está "
        "cubierto, aunque el camino tenga valles. Hoy, si sientes que te falta algo, "
        "quizás la pregunta no es qué te falta, sino en quién estás confiando para "
        "conseguirlo.",
    ),
    "Filipenses 4:13": (
        "No es una promesa de éxito, es una de contentamiento",
        "Pablo no escribió esto pensando en ganar una competencia — lo escribió en la "
        "cárcel, hablando de haber aprendido a estar contento tanto en la abundancia "
        "como en la escasez. La fortaleza que promete este versículo no es para "
        "lograr lo que queramos, es para sostenernos en cualquier circunstancia que "
        "nos toque. Eso es, en el fondo, una promesa más profunda que la que solemos "
        "citar.",
    ),
    "Salmos 46:1": (
        "Un refugio, no una salida",
        "El salmo no dice que Dios evita las tribulaciones, dice que es el amparo en "
        "medio de ellas. Hay una diferencia importante ahí: la fe cristiana no "
        "promete una vida sin tormentas, promete compañía dentro de ellas. Si hoy "
        "atraviesas algo difícil, este versículo no te pide que finjas que no pasa "
        "nada — te invita a buscar refugio mientras dura.",
    ),
    "Isaías 41:10": (
        "El temor no desaparece, pero no viaja solo",
        "Dios no le dice a Isaías «no vas a sentir miedo» — le dice «no temas, porque "
        "yo estoy contigo». Es una promesa de compañía, no de ausencia de dificultad. "
        "La próxima vez que el miedo aparezca, este versículo no te pide que lo "
        "niegues, solo que recuerdes que no lo enfrentas solo.",
    ),
    "Jeremías 29:11": (
        "Una promesa para quienes esperan, no para quienes tienen prisa",
        "Este versículo se escribió para un pueblo exiliado, que todavía tendría que "
        "esperar setenta años antes de ver ese futuro cumplirse. No es una promesa de "
        "resultados inmediatos, es una promesa de que el tiempo de espera tiene "
        "sentido. Si sientes que tu vida está en un compás de espera, esto no "
        "significa que Dios se olvidó del plan — significa que todavía no llegaste "
        "al capítulo donde se ve.",
    ),
    "Romanos 8:28": (
        "No dice que todo es bueno, dice que Dios trabaja en todo",
        "Es una distinción que vale la pena hacer: el versículo no afirma que cada "
        "cosa que nos pasa es buena en sí misma — hay dolor real, pérdidas reales. Lo "
        "que promete es que nada queda fuera del alcance de Dios para ser usado hacia "
        "un bien mayor. Eso no vuelve automáticamente livianas las cosas difíciles, "
        "pero sí cambia lo que podemos esperar de ellas con el tiempo.",
    ),
    "Proverbios 3:5-6": (
        "Confiar cuando no entendemos",
        "Fiarse de Dios «de todo corazón» es fácil de decir cuando las cosas van "
        "bien, y mucho más difícil cuando no entendemos por qué algo está pasando. "
        "Este proverbio no pide que dejemos de pensar — pide que no hagamos de "
        "nuestro propio entendimiento la última palabra. A veces el camino se "
        "endereza recién cuando soltamos la necesidad de entenderlo todo antes de "
        "dar el paso.",
    ),
    "Mateo 11:28": (
        "Una invitación a soltar, no a aguantar más",
        "Jesús no le dice a quienes están cargados «esfuércense un poco más» — les "
        "dice «vengan a mí», y promete descanso. Es una invitación distinta a la que "
        "solemos escuchar del mundo, que casi siempre pide más resistencia. Si hoy "
        "estás cansado, este versículo no es una exigencia más, es un lugar donde "
        "soltar la carga.",
    ),
    "1 Corintios 13:4-7": (
        "Una descripción, no solo un ideal romántico",
        "Estos versículos se leen mucho en bodas, pero Pablo no los escribió pensando "
        "en el amor romántico — los escribió para una comunidad que se estaba "
        "peleando entre sí. Es una lista concreta y exigente: paciencia, humildad, no "
        "llevar cuentas. Vale la pena leerla hoy pensando no en una pareja, sino en "
        "la próxima persona que te haga perder la paciencia.",
    ),
    "Salmos 118:24": (
        "Este día, no el de ayer ni el que viene",
        "Es fácil vivir alegres por lo que ya pasó o esperanzados por lo que todavía "
        "no llega, y saltarnos el día que tenemos enfrente. Este versículo es una "
        "invitación breve pero exigente: alegrarse en el día de hoy, con lo que "
        "tiene, no con lo que faltó ni con lo que falta. A veces la gratitud empieza "
        "ahí, no en las circunstancias ideales, sino en la decisión de mirar hoy con "
        "atención.",
    ),
    "Josué 1:9": (
        "El valor no es la ausencia de miedo",
        "Dios le dice esto a Josué justo cuando tiene que asumir el liderazgo después "
        "de Moisés — un momento donde cualquiera dudaría de estar a la altura. El "
        "mandato no es «no sientas miedo», es «esfuérzate y sé valiente», que da por "
        "hecho que el miedo va a estar presente. El valor bíblico no es sentirse "
        "invencible, es actuar con la certeza de que no estás solo en eso.",
    ),
    "Filipenses 4:6-7": (
        "La ansiedad no se resuelve, se entrega",
        "Pablo no dice «dejen de estar ansiosos» como si fuera una decisión simple — "
        "dice que en lugar de quedarse solos con la ansiedad, la llevemos a Dios en "
        "oración, con gratitud incluida. Lo que sigue no es la solución al problema, "
        "es una paz que «sobrepasa todo entendimiento» — una paz que no siempre tiene "
        "lógica visible, pero que sostiene igual. Si hoy la ansiedad no tiene una "
        "salida clara, este versículo ofrece al menos un lugar donde ponerla.",
    ),
    "2 Corintios 5:17": (
        "Lo viejo no se repara, se vuelve nuevo",
        "Este versículo no habla de mejorar poco a poco lo que ya éramos — habla de "
        "una transformación real, de una identidad nueva en Cristo. Eso no borra la "
        "historia de nadie, pero sí cambia qué tiene la última palabra sobre quién "
        "eres. Si cargas con una versión antigua de vos mismo que ya no querés seguir "
        "siendo, este versículo dice que ese cambio es posible, no solo deseable.",
    ),
    "Salmos 34:18": (
        "Dios está más cerca en el quebranto, no más lejos",
        "Hay una idea muy extendida de que el sufrimiento aleja a Dios, como si el "
        "dolor fuera señal de abandono. Este salmo dice justo lo contrario: es "
        "«cercano a los quebrantados de corazón». Si hoy tu corazón está roto por "
        "algo, esta promesa no es una explicación del porqué — es la certeza de que "
        "no estás más lejos de Dios por estar sufriendo, todo lo contrario.",
    ),
    "Mateo 6:33": (
        "El orden importa",
        "Jesús no dice que las demás cosas —comida, ropa, seguridad— no importen; el "
        "contexto completo de este pasaje habla justamente de esas preocupaciones "
        "cotidianas. Lo que pide es un orden: buscar primero el reino de Dios, y "
        "confiar en que lo demás se va acomodando. Es una invitación a revisar, de "
        "vez en cuando, qué es lo que realmente ocupa el primer lugar en un día "
        "común.",
    ),
    "Romanos 12:2": (
        "Transformarse empieza en cómo pensamos",
        "Pablo no pide un cambio de comportamiento superficial, pide una renovación "
        "de la mente — un cambio en la forma de pensar que después se traduce en "
        "cómo vivimos. Es más lento que copiar reglas externas, pero también más "
        "duradero. La pregunta que deja este versículo no es «¿qué debería dejar de "
        "hacer?» sino «¿qué estoy dejando que forme mi manera de pensar?».",
    ),
    "Gálatas 5:22-23": (
        "Fruto, no esfuerzo",
        "Es significativo que Pablo lo llame fruto y no logro: el fruto no se "
        "fuerza, crece con el tiempo cuando hay una raíz sana. Amor, gozo, paz, "
        "paciencia — no son metas que se alcanzan de una vez, son señales de que "
        "algo está creciendo bien por dentro. Vale la pena, hoy, mirar cuál de estos "
        "frutos se siente más escaso, no para exigírselo, sino para prestarle "
        "atención a la raíz.",
    ),
    "Salmos 27:1": (
        "¿De quién temeré?",
        "La pregunta que hace este salmo no es solo retórica — vale la pena "
        "hacérsela en serio cuando el miedo aparece. Si Jehová es la luz y la "
        "fortaleza, ¿qué otra cosa tiene el peso suficiente para quitarnos la paz? "
        "No es que el peligro deje de ser real, es que deja de tener la última "
        "palabra.",
    ),
    "Isaías 40:31": (
        "Esperar no es quedarse quieto",
        "En este versículo, esperar en Jehová no es sinónimo de no hacer nada — es "
        "lo que precede a volar, correr y caminar sin cansarse. Hay una espera "
        "activa, que no se apura ni se resigna, y que termina renovando las fuerzas "
        "en vez de agotarlas. Si estás en un tiempo de espera, esta promesa no apura "
        "el reloj, pero sí asegura que no estás perdiendo el tiempo.",
    ),
    "1 Pedro 5:7": (
        "A Él sí le importa",
        "Pedro usa una palabra fuerte: «echar», no simplemente «compartir». Es una "
        "imagen de soltar algo con intención, no de mencionarlo de pasada. La razón "
        "que da para hacerlo no es «porque no tiene remedio», sino «porque Él tiene "
        "cuidado de vosotros» — un motivo relacional, no resignado.",
    ),
    "Salmos 91:1-2": (
        "Un lugar donde habitar, no solo visitar",
        "El salmo habla de «habitar» al abrigo de Dios, no de pasar por ahí "
        "ocasionalmente. Hay una diferencia entre buscar refugio solo cuando la "
        "tormenta ya llegó, y vivir de forma constante cerca de esa fortaleza. La "
        "confianza que describe el versículo —«mi Dios, en él confiaré»— se "
        "construye con esa cercanía sostenida en el tiempo, no de un día para el "
        "otro.",
    ),
    "Mateo 5:14-16": (
        "La luz no se esconde, ilumina",
        "Jesús no manda a Sus seguidores a producir luz, les dice que ya lo son. El "
        "desafío no es convertirse en algo que no se es, es dejar de esconder lo que "
        "ya está ahí. Vale la pena preguntarse, hoy, qué «almud» —qué excusa, miedo "
        "o costumbre— podría estar tapando esa luz sin necesidad.",
    ),
    "Efesios 2:8-9": (
        "Un regalo, no una cuenta pendiente",
        "Este versículo quita una presión que muchos cargan sin darse cuenta: la "
        "idea de que hay que ganarse el amor de Dios acumulando suficientes buenas "
        "acciones. La gracia, tal como la describe Pablo, es un don — algo que se "
        "recibe, no algo que se conquista. Eso no vuelve las buenas obras "
        "innecesarias, pero sí cambia el lugar de donde salen: no de la obligación "
        "de merecer algo, sino de la libertad de ya haberlo recibido.",
    ),
    "Salmos 139:14": (
        "Formidables y maravillosas, dice el salmo — de vos",
        "Es fácil leer este versículo de forma genérica, como una frase bonita "
        "sobre la creación en general. Pero el salmo lo dice en primera persona, "
        "sobre uno mismo: «formidables, maravillosas son tus obras» hablando del "
        "propio cuerpo, la propia vida. En un día donde cueste verse con algo de "
        "valor, este versículo no pide que lo sientas — solo te recuerda que ya es "
        "verdad, lo sientas o no.",
    ),
    "Lamentaciones 3:22-23": (
        "Escrito en medio del duelo, no a pesar de él",
        "Lamentaciones es, como su nombre indica, un libro de duelo — y sin embargo, "
        "en medio de esa tristeza, aparece esta declaración de esperanza. Eso "
        "importa: la fidelidad de Dios no se afirma aquí desde la comodidad, se "
        "afirma desde el dolor más profundo. «Nuevas son cada mañana» no es una "
        "frase optimista superficial, es una verdad que sobrevivió a la pérdida.",
    ),
    "Hebreos 11:1": (
        "La fe no es certeza visible, es sustancia invisible",
        "Esta definición no promete que la fe elimina la duda o hace visible lo que "
        "todavía no se ve — dice que la fe es, en sí misma, la sustancia de lo que "
        "se espera. Es sostener algo real aunque no se pueda comprobar todavía. No "
        "hace falta tener todas las respuestas para tener fe genuina; alcanza con "
        "sostener la esperanza con las manos abiertas.",
    ),
    "Juan 14:27": (
        "Una paz distinta a la que promete el mundo",
        "La paz que ofrece el mundo casi siempre depende de que las circunstancias "
        "estén bien —ausencia de conflicto, control de la situación—. La que "
        "promete Jesús es distinta: se sostiene incluso cuando las circunstancias no "
        "cambian. «No se turbe vuestro corazón» no es una orden de sentir calma por "
        "obligación, es una invitación a apoyarse en un tipo de paz que no depende "
        "de que todo esté resuelto.",
    ),
    "Salmos 121:1-2": (
        "Mirar hacia arriba antes de buscar la solución",
        "Alzar los ojos a los montes, en el contexto original, podía ser una imagen "
        "de peligro tanto como de esperanza. El salmista resuelve la ambigüedad de "
        "inmediato: su socorro no viene de cualquier lugar alto, viene "
        "específicamente de Jehová, hacedor de los cielos y la tierra. Antes de "
        "buscar ayuda en cualquier otro lado, vale la pena preguntarse hacia dónde "
        "estamos mirando primero.",
    ),
    "1 Juan 4:19": (
        "El amor como respuesta, no como esfuerzo",
        "Este versículo pone el orden en su lugar: no amamos primero para ganarnos "
        "el amor de Dios, amamos porque ya fuimos amados primero. Es una base "
        "distinta para amar a los demás — no desde la carencia, tratando de "
        "conseguir algo, sino desde algo que ya se recibió. Hoy, amar a alguien "
        "difícil puede doler menos si se hace desde ese lugar, no desde la "
        "obligación.",
    ),
}

db = SessionLocal()

verse_by_reference: dict[str, Verse] = {}
for book, chapter, vstart, vend, reference, text in VERSES:
    verse = db.query(Verse).filter(Verse.reference == reference).first()
    if verse is None:
        verse = Verse(
            book=book,
            chapter=chapter,
            verse_start=vstart,
            verse_end=vend,
            reference=reference,
            text=text,
            translation="RVA1909",
        )
        db.add(verse)
        db.flush()
    verse_by_reference[reference] = verse

reflection_by_reference: dict[str, Reflection] = {}
for reference, verse in verse_by_reference.items():
    existing = db.query(Reflection).filter(Reflection.verse_id == verse.id).first()
    if existing:
        reflection_by_reference[reference] = existing
        continue
    title, body = REFLECTIONS[reference]
    reflection = Reflection(
        verse_id=verse.id,
        title=title,
        body=body,
        status="ai_generated",
        source="ai_assisted",
    )
    db.add(reflection)
    db.flush()
    reflection_by_reference[reference] = reflection

db.commit()

# Fechas con un favorito de algun usuario apuntando a ellas: nunca se tocan
# (cambiarles el contenido cambiaria retroactivamente lo que esa persona
# guardo como favorito).
favorited_daily_verse_ids = {f.daily_verse_id for f in db.query(Favorite).all()}
existing = {d.date: d for d in db.query(DailyVerse).all()}
protected_dates = {dt for dt, entry in existing.items() if entry.id in favorited_daily_verse_ids}

# Juan 3:16 ya esta sembrado y (en este caso) protegido por un favorito real -
# no hace falta re-programarlo, usamos las 29 reflexiones restantes.
references_to_schedule = [v[4] for v in VERSES if v[4] != "Juan 3:16"] if protected_dates else [
    v[4] for v in VERSES
]

start_date = min(existing.keys()) if existing else date.today()
scheduled = 0
current = start_date
for reference in references_to_schedule:
    while current in protected_dates:
        current += timedelta(days=1)

    verse = verse_by_reference[reference]
    reflection = reflection_by_reference[reference]

    entry = existing.get(current)
    if entry:
        entry.verse_id = verse.id
        entry.reflection_id = reflection.id
    else:
        db.add(DailyVerse(date=current, verse_id=verse.id, reflection_id=reflection.id))

    scheduled += 1
    current += timedelta(days=1)

db.commit()
print(f"Sembrados {len(verse_by_reference)} versiculos/reflexiones, {scheduled} dias programados "
      f"desde {start_date}. Fechas protegidas (con favoritos, no tocadas): {protected_dates}")
