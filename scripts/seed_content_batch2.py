"""Segundo lote de contenido: 90 versiculos (RVA1909, dominio publico) y
reflexiones nuevas, pensadas para dar ~3 meses de colchon adicional sobre
las que ya existen (ver scripts/seed_content.py para las primeras 30).

A diferencia de seed_content.py, este script NO programa fechas en
DailyVerse directamente: desde que existe el cron de Railway
(backend/scripts/auto_schedule_verse.py, corre a diario) el colchon de
dias se llena solo tomando reflexiones en status="reviewed". Este script
solo siembra Verse + Reflection en status="ai_generated" -- quedan
pendientes de tu revision en el admin (/reflections). Al pasarlas a
"reviewed", el cron las va a programar automaticamente en los proximos
dias, sin necesidad de asignarles fecha a mano.

El texto de los versiculos viene del dump SQL de la RVA1909 publicado en
github.com/iglesianazaret/biblia-reina-valera-1909-base-datos-sql
(dominio publico), extraido directamente del archivo (no transcrito de
memoria), igual que en el primer lote.

Verificado sin superposicion con las 30 referencias del primer lote.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.database import SessionLocal
from app.models import Reflection, Verse

# (book, chapter, verse_start, verse_end, reference, text)
VERSES = [
    ("Génesis", 28, 15, None, "Génesis 28:15",
     "Y he aquí, yo soy contigo, y te guardaré por donde quiera que fueres, y te "
     "volveré a esta tierra; porque no te dejaré hasta tanto que haya hecho lo que "
     "te he dicho."),
    ("Éxodo", 14, 14, None, "Éxodo 14:14",
     "Jehová peleará por vosotros, y vosotros estaréis quedos."),
    ("Éxodo", 33, 14, None, "Éxodo 33:14",
     "Y él dijo: Mi rostro irá contigo, y te haré descansar."),
    ("Deuteronomio", 31, 6, None, "Deuteronomio 31:6",
     "Esforzaos y cobrad ánimo; no temáis, ni tengáis miedo de ellos: que Jehová tu "
     "Dios es el que va contigo: no te dejará ni te desamparará."),
    ("Deuteronomio", 31, 8, None, "Deuteronomio 31:8",
     "Y Jehová es el que va delante de ti; él será contigo, no te dejará, ni te "
     "desamparará; no temas, ni te intimides."),
    ("Josué", 24, 15, None, "Josué 24:15",
     "Y si mal os parece servir a Jehová, escogeos hoy a quién sirváis; si a los "
     "dioses a quienes siervieron vuestros padres, cuando estuvieron de esotra "
     "parte del río, o a los dioses de los Amorrheos en cuya tierra habitáis: que "
     "yo y mi casa serviremos a Jehová."),
    ("1 Samuel", 16, 7, None, "1 Samuel 16:7",
     "Y Jehová respondió a Samuel: No mires a su parecer, ni a lo grande de su "
     "estatura, porque yo lo desecho; porque Jehová mira no lo que el hombre mira; "
     "pues que el hombre mira lo que está delante de sus ojos, mas Jehová mira el "
     "corazón."),
    ("1 Reyes", 19, 12, None, "1 Reyes 19:12",
     "Y tras el terremoto un fuego: mas Jehová no estaba en el fuego. Y tras el "
     "fuego un silvo apacible y delicado."),
    ("1 Crónicas", 16, 11, None, "1 Crónicas 16:11",
     "Buscad a Jehová y su fortaleza; Buscad su rostro continuamente."),
    ("2 Crónicas", 7, 14, None, "2 Crónicas 7:14",
     "Si se humillare mi pueblo, sobre los cuales ni nombre es invocado, y oraren, "
     "y buscaren mi rostro, y se convirtieren de sus malos caminos; entonces yo "
     "oiré desde los cielos, y perdonaré sus pecados, y sanaré su tierra."),
    ("Nehemías", 8, 10, None, "Nehemías 8:10",
     "Díjoles luego: Id, comed grosuras, y bebed vino dulce, y enviad porciones a "
     "los que no tienen prevenido; porque día santo es a nuestro Señor: y no os "
     "entristezcáis, porque el gozo de Jehová es vuestra fortaleza."),
    ("Job", 19, 25, None, "Job 19:25",
     "Yo sé que mi Redentor vive, Y al fin se levantará sobre el polvo:"),
    ("Job", 42, 2, None, "Job 42:2",
     "Yo conozco que todo lo puedes, Y que no hay pensamiento que se esconda de "
     "ti."),
    ("Proverbios", 4, 23, None, "Proverbios 4:23",
     "Sobre toda cosa guardada guarda tu corazón; Porque de él mana la vida."),
    ("Proverbios", 16, 3, None, "Proverbios 16:3",
     "Encomienda a Jehová tus obras, Y tus pensamientos serán afirmados."),
    ("Proverbios", 16, 9, None, "Proverbios 16:9",
     "El corazón del hombre piensa su camino: Mas Jehová endereza sus pasos."),
    ("Proverbios", 17, 22, None, "Proverbios 17:22",
     "El corazón alegre produce buena disposición: Mas el espíritu triste seca los "
     "huesos."),
    ("Proverbios", 18, 10, None, "Proverbios 18:10",
     "Torre fuerte es el nombre de Jehová: A él correrá el justo, y será "
     "levantado."),
    ("Proverbios", 22, 6, None, "Proverbios 22:6",
     "Instruye al niño en su carrera: Aun cuando fuere viejo no se apartará de "
     "ella."),
    ("Eclesiastés", 3, 1, None, "Eclesiastés 3:1",
     "Para todas las cosas hay sazón, y todo lo que se quiere debajo del cielo, "
     "tiene su tiempo:"),
    ("Salmos", 1, 1, 3, "Salmos 1:1-3",
     "Bienaventurado el varón que no anduvo en consejo de malos, Ni estuvo en "
     "camino de pecadores, Ni en silla de escarnecedores se ha sentado; Antes en "
     "la ley de Jehová está su delicia, Y en su ley medita de día y de noche. Y "
     "será como el árbol plantado junto a arroyos de aguas, Que da su fruto en su "
     "tiempo, Y su hoja no cae; Y todo lo que hace, prosperará."),
    ("Salmos", 16, 11, None, "Salmos 16:11",
     "Me mostrarás la senda de la vida: Hartura de alegrías hay con tu rostro; "
     "Deleites en tu diestra para siempre."),
    ("Salmos", 19, 1, None, "Salmos 19:1",
     "Los cielos cuentan la gloria de Dios, Y la expansión denuncia la obra de sus "
     "manos."),
    ("Salmos", 25, 4, 5, "Salmos 25:4-5",
     "Muéstrame, oh Jehová, tus caminos; Enséñame tus sendas. Encamíname en tu "
     "verdad, y enséñame; Porque tú eres el Dios de mi salud: En ti he esperado "
     "todo el día."),
    ("Salmos", 30, 5, None, "Salmos 30:5",
     "Porque un momento será su furor; Mas en su voluntad está la vida: Por la "
     "tarde durará el lloró, Y a la mañana vendrá la alegría."),
    ("Salmos", 32, 8, None, "Salmos 32:8",
     "Te haré entender, y te enseñaré el camino en que debes andar: Sobre ti "
     "fijaré mis ojos."),
    ("Salmos", 34, 8, None, "Salmos 34:8",
     "Gustad, y ved que es bueno Jehová: Dichoso el hombre que confiará en él."),
    ("Salmos", 37, 4, None, "Salmos 37:4",
     "Pon asimismo tu delicia en Jehová, Y él te dará las peticiones de tu "
     "corazón."),
    ("Salmos", 55, 22, None, "Salmos 55:22",
     "Echa sobre Jehová tu carga, y él te sustentará; No dejará para siempre "
     "caído al justo."),
    ("Salmos", 62, 1, 2, "Salmos 62:1-2",
     "En Dios solamente está callada mi alma: De él viene mi salud. Él solamente "
     "es mi fuerte, y mi salud; Es mi refugio, no resbalaré mucho."),
    ("Salmos", 90, 12, None, "Salmos 90:12",
     "Enséñanos de tal modo a contar nuestros días, Que traigamos al corazón "
     "sabiduría."),
    ("Salmos", 107, 1, None, "Salmos 107:1",
     "Alabad a Jehová, porque es bueno; Porque para siempre es su misericordia."),
    ("Salmos", 119, 105, None, "Salmos 119:105",
     "Lámpara es a mis pies tu palabra, Y lumbrera a mi camino."),
    ("Salmos", 147, 3, None, "Salmos 147:3",
     "Él sana a los quebrantados de corazón, Y liga sus heridas."),
    ("Isaías", 26, 3, None, "Isaías 26:3",
     "Tú le guardarás en completa paz, cuyo pensamiento en ti persevera; porque en "
     "ti se ha confiado."),
    ("Isaías", 30, 15, None, "Isaías 30:15",
     "Porque así dijo el Señor Jehová, el Santo de Israel: En descanso y en "
     "reposo seréis salvos; en quietud y en confianza será vuestra fortaleza. Y no "
     "quisisteis,"),
    ("Isaías", 43, 2, None, "Isaías 43:2",
     "Cuando pasares por las aguas, yo seré contigo; y por los ríos, no te "
     "anegarán. Cuando pasares por el fuego, no te quemarás, ni la llama arderá "
     "en ti."),
    ("Isaías", 53, 5, None, "Isaías 53:5",
     "Mas él herido fue por nuestras rebeliones, molido por nuestros pecados: el "
     "castigo de nuestra paz sobre él; y por su llaga fuimos nosotros curados."),
    ("Isaías", 55, 8, 9, "Isaías 55:8-9",
     "Porque mis pensamientos no son vuestros pensamientos, ni vuestros caminos "
     "mis caminos, dijo Jehová. Como son más altos los cielos que la tierra, así "
     "son mis caminos más altos que vuestros caminos, y mis pensamientos más que "
     "vuestros pensamientos."),
    ("Isaías", 61, 1, None, "Isaías 61:1",
     "El espíritu del Señor Jehová es sobre mí, porque me ungió Jehová; hame "
     "enviado a predicar buenas nuevas a los abatidos, a vendar a los "
     "quebrantados de corazón, a publicar libertad a los cautivos, y a los presos "
     "abertura de la cárcel;"),
    ("Jeremías", 17, 7, 8, "Jeremías 17:7-8",
     "Bendito el varón que se fía en Jehová, y cuya confianza es Jehová. Porque "
     "él será como el árbol plantado junto a las aguas, que junto a la corriente "
     "echará sus raíces, y no verá cuando viniere el calor, sino que su hoja "
     "estará verde; y en el año de sequía no se fatigará, ni dejará de hacer "
     "fruto."),
    ("Ezequiel", 36, 26, None, "Ezequiel 36:26",
     "Y os daré corazón nuevo, y pondré espíritu nuevo dentro de vosotros; y "
     "quitaré de vuestra carne el corazón de piedra, y os daré corazón de carne."),
    ("Daniel", 3, 17, 18, "Daniel 3:17-18",
     "He aquí nuestro Dios a quien honramos, puede librarnos del horno de fuego "
     "ardiendo; y de tu mano, oh rey, nos librará. Y si no, sepas, oh rey, que tu "
     "dios no adoraremos, ni tampoco honraremos la estatua que has levantado."),
    ("Miqueas", 6, 8, None, "Miqueas 6:8",
     "Oh hombre, él te ha declarado qué sea lo bueno, y qué pida de ti Jehová: "
     "solamente hacer juicio, y amar misericordia, y humillarte para andar con tu "
     "Dios."),
    ("Sofonías", 3, 17, None, "Sofonías 3:17",
     "Jehová en medio de ti, poderoso, él salvará; gozarase sobre ti con alegría, "
     "callará de amor, se regocijará sobre ti con cantar."),
    ("Mateo", 5, 4, None, "Mateo 5:4",
     "Bienaventurados los que lloran: porque ellos recibirán consolación."),
    ("Mateo", 18, 20, None, "Mateo 18:20",
     "Porque donde están dos o tres congregados en mi nombre, allí estoy en medio "
     "de ellos."),
    ("Mateo", 7, 7, None, "Mateo 7:7",
     "Pedid, y se os dará; buscad, y hallaréis; llamad, y se os abrirá."),
    ("Mateo", 19, 26, None, "Mateo 19:26",
     "Y mirándolos Jesús, les dijo: Para con los hombres imposible es esto; mas "
     "para con Dios todo es posible."),
    ("Mateo", 28, 20, None, "Mateo 28:20",
     "Enseñándoles que guarden todas las cosas que os he mandado: y he aquí, yo "
     "estoy con vosotros todos los días, hasta el fin del mundo. Amén."),
    ("Marcos", 9, 23, None, "Marcos 9:23",
     "Y Jesús le dijo: Si puedes creer, al que cree todo es posible."),
    ("Marcos", 10, 27, None, "Marcos 10:27",
     "Entonces Jesús mirándolos, dice: Para los hombres es imposible; mas para "
     "Dios, no; porque todas las cosas son posibles para Dios."),
    ("Marcos", 11, 24, None, "Marcos 11:24",
     "Por tanto, os digo que todo lo que orando pidiereis, creed que lo "
     "recibiréis, y os vendrá."),
    ("Lucas", 1, 37, None, "Lucas 1:37",
     "Porque ninguna cosa es imposible para Dios."),
    ("Lucas", 6, 38, None, "Lucas 6:38",
     "Dad, y se os dará; medida buena, apretada, remecida, y rebosando darán en "
     "vuestro seno: porque con la misma medida que midiereis, os será vuelto a "
     "medir."),
    ("Lucas", 15, 20, None, "Lucas 15:20",
     "Y levantándose, vino a su padre. Y como aun estuviese lejos, violo su "
     "padre, y fue movido a misericordia, y corrió, y echose sobre su cuello, y "
     "besole."),
    ("Lucas", 18, 1, None, "Lucas 18:1",
     "Y propúsoles también una parábola sobre que es necesario orar siempre, y no "
     "desmayar,"),
    ("Juan", 1, 12, None, "Juan 1:12",
     "Mas a todos los que le recibieron, dioles potestad de ser hechos hijos de "
     "Dios, a los que creen en su nombre:"),
    ("Juan", 8, 12, None, "Juan 8:12",
     "Y habloles Jesús otra vez, diciendo: Yo soy la luz del mundo: el que me "
     "sigue, no andará en tinieblas, mas tendrá la lumbre de la vida."),
    ("Juan", 10, 10, None, "Juan 10:10",
     "El ladrón no viene sino para hurtar, y matar, y destruir: yo he venido para "
     "que tengan vida, y para que la tengan en abundancia."),
    ("Juan", 16, 33, None, "Juan 16:33",
     "Estas cosas os he hablado, para que en mí tengáis paz. En el mundo tendréis "
     "aflicción: mas confiad, yo he vencido al mundo."),
    ("Hechos", 1, 8, None, "Hechos 1:8",
     "Mas recibiréis la virtud del Espíritu Santo que vendrá sobre vosotros; y me "
     "seréis testigos en Jerusalem, en toda Judea, y Samaria, y hasta lo último "
     "de la tierra."),
    ("Hechos", 4, 12, None, "Hechos 4:12",
     "Y en ningún otro hay salud; porque no hay otro nombre debajo del cielo, "
     "dado a los hombres, en que podamos ser salvos."),
    ("Romanos", 5, 8, None, "Romanos 5:8",
     "Mas Dios encarece su caridad para con nosotros, porque siendo aún "
     "pecadores, Cristo murió por nosotros."),
    ("Romanos", 8, 1, None, "Romanos 8:1",
     "Ahora pues, ninguna condenación hay para los que están en Cristo Jesús, los "
     "que no andan conforme a la carne, mas conforme al espíritu."),
    ("Romanos", 8, 38, 39, "Romanos 8:38-39",
     "Por lo cual estoy cierto que ni la muerte, ni la vida, ni ángeles, ni "
     "principados, ni potestades, ni lo presente, ni lo por venir, Ni lo alto, ni "
     "lo bajo, ni ninguna criatura nos podrá apartar del amor de Dios, que es en "
     "Cristo Jesús Señor nuestro."),
    ("Romanos", 10, 9, None, "Romanos 10:9",
     "Que si confesares con tu boca al Señor Jesús, y creyeres en tu corazón que "
     "Dios le levantó de los muertos, serás salvo."),
    ("1 Corintios", 10, 13, None, "1 Corintios 10:13",
     "No os ha tomado tentación, sino humana: mas fiel es Dios, que no os dejará "
     "ser tentados más de lo que podéis llevar; antes dará también juntamente con "
     "la tentación la salida, para que podáis aguantar."),
    ("1 Corintios", 15, 58, None, "1 Corintios 15:58",
     "Así que, hermanos míos amados, estad firmes y constantes, creciendo en la "
     "obra del Señor siempre, sabiendo que vuestro trabajo en el Señor no es "
     "vano."),
    ("1 Corintios", 16, 14, None, "1 Corintios 16:14",
     "Todas vuestras cosas sean hechas con caridad."),
    ("2 Corintios", 4, 16, 18, "2 Corintios 4:16-18",
     "Por tanto, no desmayamos: antes aunque este nuestro hombre exterior se va "
     "desgastando, el interior empero se renueva de día en día. Porque lo que al "
     "presente es momentáneo y leve de nuestra tribulación, nos obra un "
     "sobremanera alto y eterno peso de gloria; No mirando nosotros a las cosas "
     "que se ven, sino a las que no se ven: porque las cosas que se ven son "
     "temporales, mas las que no se ven son eternas."),
    ("2 Corintios", 12, 9, None, "2 Corintios 12:9",
     "Y me ha dicho: Bástate mi gracia; porque mi potencia en la flaqueza se "
     "perfecciona. Por tanto, de buena gana me gloriaré más bien en mis "
     "flaquezas, porque habite en mí la potencia de Cristo."),
    ("Gálatas", 2, 20, None, "Gálatas 2:20",
     "Con Cristo estoy juntamente crucificado, y vivo, no ya yo, mas vive Cristo "
     "en mí: y lo que ahora vivo en la carne, lo vivo en la fe del Hijo de Dios, "
     "el cual me amó, y se entregó a sí mismo por mí."),
    ("Gálatas", 6, 9, None, "Gálatas 6:9",
     "No nos cansemos, pues, de hacer bien; que a su tiempo segaremos, si no "
     "hubiéremos desmayado."),
    ("Efesios", 2, 10, None, "Efesios 2:10",
     "Porque somos hechura suya, criados en Cristo Jesús para buenas obras, las "
     "cuales Dios preparó para que anduviésemos en ellas."),
    ("Efesios", 3, 20, None, "Efesios 3:20",
     "Y a Aquel que es poderoso para hacer todas las cosas mucho más "
     "abundantemente de lo que pedimos o entendemos, por la potencia que obra en "
     "nosotros,"),
    ("Efesios", 4, 32, None, "Efesios 4:32",
     "Antes sed los unos con los otros benignos, misericordiosos, perdonándoos "
     "los unos a los otros, como también Dios os perdonó en Cristo."),
    ("Filipenses", 1, 6, None, "Filipenses 1:6",
     "Estando confiado de esto, que el que comenzó en vosotros la buena obra, la "
     "perfeccionará hasta el día de Jesucristo;"),
    ("Filipenses", 4, 4, None, "Filipenses 4:4",
     "Gozaos en el Señor siempre: otra vez digo: Que os gocéis."),
    ("Colosenses", 3, 23, None, "Colosenses 3:23",
     "Y todo lo que hagáis, hacedlo de ánimo, como al Señor, y no a los hombres;"),
    ("1 Tesalonicenses", 5, 16, 18, "1 Tesalonicenses 5:16-18",
     "Estad siempre gozosos. Orad sin cesar. Dad gracias en todo; porque esta es "
     "la voluntad de Dios para con vosotros en Cristo Jesús."),
    ("2 Timoteo", 1, 7, None, "2 Timoteo 1:7",
     "Porque no nos ha dado Dios el espíritu de temor, sino el de fortaleza, y de "
     "amor, y de templanza."),
    ("Hebreos", 4, 16, None, "Hebreos 4:16",
     "Lleguémonos pues confiadamente al trono de la gracia, para alcanzar "
     "misericordia, y hallar gracia para el oportuno socorro."),
    ("Santiago", 1, 5, None, "Santiago 1:5",
     "Y si alguno de vosotros tiene falta de sabiduría, demándela a Dios, el cual "
     "da a todos abundantemente, y no zahiere; y le será dada."),
    ("Santiago", 1, 19, None, "Santiago 1:19",
     "Por esto, mis amados hermanos, todo hombre sea pronto para oír, tardío "
     "para hablar, tardío para airarse:"),
    ("1 Pedro", 1, 3, None, "1 Pedro 1:3",
     "Bendito el Dios y Padre de nuestro Señor Jesucristo, que según su grande "
     "misericordia nos ha regenerado en esperanza viva, por la resurrección de "
     "Jesucristo de los muertos,"),
    ("1 Pedro", 2, 9, None, "1 Pedro 2:9",
     "Mas vosotros sois linaje escogido, real sacerdocio, gente santa, pueblo "
     "adquirido, para que anunciéis las virtudes de aquel que os ha llamado de "
     "las tinieblas a su luz admirable."),
    ("1 Juan", 1, 9, None, "1 Juan 1:9",
     "Si confesamos nuestros pecados, Él es fiel y justo para que nos perdone "
     "nuestros pecados, y nos limpie de toda maldad."),
    ("Apocalipsis", 3, 20, None, "Apocalipsis 3:20",
     "He aquí, yo estoy a la puerta y llamo: si alguno oyere mi voz y abriere la "
     "puerta, entraré a Él, y cenaré con Él, y Él conmigo."),
    ("Apocalipsis", 21, 4, None, "Apocalipsis 21:4",
     "Y limpiará Dios toda lágrima de los ojos de ellos; y la muerte no será más; "
     "y no habrá más llanto, ni clamor, ni dolor: porque las primeras cosas son "
     "pasadas."),
]

# reference -> (title, body, mood_tags). mood_tags solo de la lista canonica
# en apps/mobile/src/lib/moodTags.ts (ansiedad, tristeza, duelo, gratitud,
# esperanza, duda, fortaleza, paz, gozo, agotamiento).
REFLECTIONS = {
    "Génesis 28:15": (
        "Una promesa hecha a alguien que estaba huyendo",
        "Jacob no recibe esta promesa en un templo ni en un momento de fe "
        "ejemplar: la recibe dormido en el suelo, huyendo de su hermano, con "
        "motivos reales para tener miedo. Dios no espera a que ordene su vida "
        "para prometerle compañía, se la da en medio de la fuga. «Te guardaré "
        "por donde quiera que fueres» no es una garantía de que el camino será "
        "cómodo, es la certeza de que no lo recorrerás solo. Si hoy estás en "
        "una etapa de tu vida que preferirías no estar viviendo, esta promesa "
        "no pide que primero la merezcas.",
        ["ansiedad", "esperanza", "fortaleza"],
    ),
    "Éxodo 14:14": (
        "Estar quieto también es una forma de fe",
        "Israel está atrapado entre el mar y el ejército egipcio, y la "
        "instrucción no es «luchen» ni «corran»: es «estad quedos». Hay "
        "momentos donde la fe no se parece a la acción, se parece a soltar el "
        "control y dejar que Dios actúe primero. Eso no es pasividad cómoda: "
        "exige confiar cuando todo el instinto pide resolver algo con las "
        "propias manos. Si hoy sientes que no puedes hacer nada frente a lo "
        "que enfrentas, este versículo no te condena por eso, te recuerda que "
        "no todo depende de tu esfuerzo.",
        ["ansiedad", "paz"],
    ),
    "Éxodo 33:14": (
        "No promete el destino, promete la compañía",
        "Moisés no pide direcciones ni un plan detallado, pide la presencia "
        "de Dios en el camino, y eso es exactamente lo que recibe. La "
        "respuesta no resuelve la incertidumbre del futuro, la sostiene con "
        "algo más importante: no ir solo. Es fácil pedir certezas cuando lo "
        "que en realidad se necesita es compañía. Hoy, si no tienes claro "
        "hacia dónde vas, esta promesa no llena el mapa, llena el camino.",
        ["paz", "ansiedad"],
    ),
    "Deuteronomio 31:6": (
        "El valor tiene un motivo, no es solo una orden",
        "«Esforzaos y cobrad ánimo» suena a exigencia, pero la frase completa "
        "no termina ahí, termina explicando el porqué: Dios va contigo. No es "
        "un llamado a fingir fortaleza que no tienes, es una razón concreta "
        "para tenerla. El miedo que sientes ante lo que viene no desaparece "
        "por decreto, pero sí cambia de tamaño cuando se mira junto a esa "
        "promesa. Hoy, si te toca enfrentar algo para lo que no te sientes "
        "preparado, este versículo no te pide que lo estés solo.",
        ["fortaleza", "ansiedad"],
    ),
    "Deuteronomio 31:8": (
        "Él va delante, no solo al lado",
        "Hay una diferencia entre alguien que te acompaña y alguien que va "
        "delante abriendo camino, y este versículo promete lo segundo. No es "
        "solo compañía en el sufrimiento, es alguien adelantándose a lo que "
        "todavía no llega. Eso no elimina la incertidumbre de lo que hay más "
        "adelante, pero cambia quién la enfrenta primero. Si hoy te preocupa "
        "lo que no puedes ver todavía, esta promesa no te pide anticiparlo tú "
        "solo.",
        ["ansiedad", "fortaleza"],
    ),
    "Josué 24:15": (
        "Una decisión que no se puede posponer indefinidamente",
        "Josué no pregunta a su pueblo qué opina en abstracto, les pide que "
        "decidan hoy a quién van a servir, y él mismo se compromete primero "
        "con su propia casa. No hay una opción neutral en la propuesta: "
        "servir a algo, o a otra cosa, siempre se está sirviendo a alguien. "
        "Vale la pena hacerse la misma pregunta de vez en cuando, no como un "
        "examen de fe perfecta, sino como una revisión honesta de qué ocupa "
        "realmente el lugar central de una vida.",
        ["duda"],
    ),
    "1 Samuel 16:7": (
        "Lo que Dios mira cuando nosotros miramos otra cosa",
        "Samuel está a punto de ungir al candidato más impresionante a "
        "simple vista, y Dios lo detiene: no es ese. La corrección no es "
        "sobre el candidato, es sobre el criterio: el ser humano juzga por lo "
        "que se ve, Dios mira el corazón. Es una idea incómoda en una cultura "
        "que premia la imagen: lo que más se nota no siempre es lo que más "
        "importa. Si hoy te sientes menos por no destacar de forma visible, "
        "este versículo mide distinto.",
        ["duda", "gratitud"],
    ),
    "1 Reyes 19:12": (
        "No en el terremoto, sino en el silencio",
        "Elías espera encontrar a Dios en el viento fuerte, el terremoto o "
        "el fuego, y no está ahí: está en «un silvo apacible y delicado». "
        "Después de un colapso emocional real (el capítulo anterior lo "
        "muestra pidiendo morir), lo que Elías recibe no es un espectáculo, "
        "es una voz suave. A veces buscamos a Dios en lo dramático cuando en "
        "realidad se hace presente en lo callado. Si hoy tu oración se siente "
        "más silenciosa que espectacular, quizás ahí es exactamente donde hay "
        "que escuchar.",
        ["paz", "agotamiento"],
    ),
    "1 Crónicas 16:11": (
        "Buscar, no solo encontrar una vez",
        "El mandato no es «busquen a Jehová» en pasado, como algo que ya se "
        "resolvió, es «continuamente», una búsqueda que no termina en un solo "
        "momento de decisión. Eso cambia la expectativa: la cercanía con Dios "
        "no es un logro que se archiva, es una práctica que se sostiene. No "
        "hace falta sentir que ya se llegó a algún lugar fijo; alcanza con "
        "seguir buscando hoy, otra vez.",
        ["esperanza", "paz"],
    ),
    "2 Crónicas 7:14": (
        "La restauración empieza con humildad, no con un plan perfecto",
        "La promesa no depende de que el pueblo tenga primero todas las "
        "respuestas o una estrategia impecable, depende de humillarse, orar, "
        "buscar y volver. Son pasos posibles incluso en medio del desorden. "
        "Es fácil pensar que hace falta resolver todo antes de acercarse a "
        "Dios, cuando en realidad el acercarse es, muchas veces, el primer "
        "paso hacia el orden, no el último.",
        ["esperanza", "duda"],
    ),
    "Nehemías 8:10": (
        "El gozo no es un lujo, es una fuerza",
        "El pueblo llora al escuchar la ley, conmovido por lo que no habían "
        "cumplido, y Nehemías los detiene: no es día de tristeza, es día de "
        "gozo, y ese gozo, dice, es su fortaleza. No niega el motivo real de "
        "la tristeza, pero prioriza otra cosa: la alegría como algo que "
        "sostiene, no como un premio por portarse bien. Si hoy sientes que no "
        "tienes derecho a alegrarte en medio de tus fallas, este versículo "
        "invita a otra lectura.",
        ["gozo", "tristeza"],
    ),
    "Job 19:25": (
        "Una certeza sostenida desde el fondo del dolor",
        "Job dice esto, «yo sé que mi Redentor vive», no desde la comodidad, "
        "sino habiendo perdido casi todo lo que tenía, incluida la salud y a "
        "sus hijos. No es una frase optimista fácil de decir, es una "
        "convicción que sobrevive intacta en medio de la pérdida más real. "
        "Eso le da un peso distinto: la esperanza de Job no depende de que su "
        "situación mejore primero.",
        ["esperanza", "duelo"],
    ),
    "Job 42:2": (
        "Reconocer los límites, no tener todas las respuestas",
        "Esta frase llega al final del libro, después de capítulos donde Job "
        "exige explicaciones y Dios no se las da del todo, solo le muestra la "
        "magnitud de lo que no controla. La conclusión de Job no es que "
        "entendió todo, es que reconoce que Dios puede todo, aunque el "
        "porqué siga sin resolverse. A veces la fe no termina en respuestas, "
        "termina en confianza sin ellas.",
        ["duda", "fortaleza"],
    ),
    "Proverbios 4:23": (
        "Lo que se guarda primero, antes que todo lo demás",
        "El proverbio no pide cuidar las acciones o las palabras primero, "
        "pide cuidar el corazón, porque de ahí, dice, mana la vida. Es una "
        "prioridad distinta a la que solemos usar, más enfocada en corregir "
        "comportamientos que en revisar qué los origina. Vale la pena "
        "preguntarse, de vez en cuando, qué se está dejando entrar sin filtro "
        "al lugar de donde sale todo lo demás.",
        ["fortaleza"],
    ),
    "Proverbios 16:3": (
        "Encomendar antes de tener el plan resuelto",
        "El proverbio no promete que las obras encomendadas a Dios saldrán "
        "como se planearon, promete que los pensamientos serán afirmados, "
        "sostenidos. Es una paz distinta a la de tener control total: la de "
        "confiar el resultado mientras se hace el trabajo. Si hoy te cuesta "
        "soltar algo que estás intentando resolver a la fuerza, esto no pide "
        "que dejes de esforzarte, pide que no cargues solo con el resultado.",
        ["ansiedad", "fortaleza"],
    ),
    "Proverbios 16:9": (
        "Planear no es lo mismo que tener el control",
        "El proverbio no dice que planear esté mal, dice que, al final, es "
        "Jehová quien endereza los pasos, no el plan mismo. Hay lugar para "
        "pensar el camino y también para que se tuerza de formas que no se "
        "esperaban. Si algo en tu vida no salió como lo planeaste, este "
        "versículo no lo llama fracaso, lo llama un paso que igual fue "
        "enderezado.",
        ["duda", "esperanza"],
    ),
    "Proverbios 17:22": (
        "El cuerpo también carga lo que el ánimo siente",
        "El proverbio conecta algo que a veces se separa: un espíritu "
        "triste, dice, seca los huesos, no solo entristece el alma. Es una "
        "forma antigua de decir algo que hoy se entiende mejor: el ánimo y el "
        "cuerpo no viven en compartimentos aislados. Cuidar la alegría no es "
        "superficial, es parte de cuidar la vida entera. Si hoy el cuerpo se "
        "siente cansado sin causa clara, vale la pena preguntarse también "
        "cómo está el ánimo.",
        ["gozo", "tristeza"],
    ),
    "Proverbios 18:10": (
        "Un refugio al que se corre, no uno que se visita",
        "La imagen no es de un lugar pasivo, es de alguien corriendo hacia "
        "una torre fuerte para ponerse a salvo. Hay una acción de por medio: "
        "el nombre de Jehová no protege desde lejos, protege a quien decide "
        "acercarse en el momento en que lo necesita. Si hoy sientes que "
        "necesitas ese refugio, el proverbio no pide que esperes a estar en "
        "calma para buscarlo.",
        ["fortaleza", "ansiedad"],
    ),
    "Proverbios 22:6": (
        "Una promesa a largo plazo, no de resultado inmediato",
        "El proverbio habla de instruir a un niño, pero la promesa, «aun "
        "cuando fuere viejo no se apartará», mira décadas hacia adelante, no "
        "la semana siguiente. Es un recordatorio para quienes siembran algo "
        "en otra persona sin ver todavía el fruto: lo que se enseña con "
        "constancia no siempre se nota de inmediato, pero deja una huella que "
        "dura.",
        ["esperanza"],
    ),
    "Eclesiastés 3:1": (
        "Hay tiempo para esto también",
        "El versículo no dice que todos los tiempos sean buenos, dice que "
        "todos tienen su lugar: el libro completo enumera después tiempos de "
        "llorar, de guardar luto, de callar. Es un permiso implícito: no "
        "todas las temporadas de la vida tienen que sentirse productivas o "
        "alegres para tener sentido. Si hoy atraviesas una etapa difícil, "
        "este versículo no te apura a salir de ella antes de tiempo.",
        ["duelo", "esperanza"],
    ),
    "Salmos 1:1-3": (
        "Lo que se planta cerca del agua no depende de la sequía",
        "El salmo no promete que la vida del árbol junto al arroyo estará "
        "libre de calor o de temporadas difíciles, promete que su raíz tiene "
        "de dónde sostenerse. La diferencia no está en evitar las "
        "dificultades, está en dónde se está plantado. Meditar «de día y de "
        "noche» no es una obligación religiosa pesada, es la raíz que "
        "permite que, pase lo que pase alrededor, la hoja no se caiga.",
        ["fortaleza", "esperanza"],
    ),
    "Salmos 16:11": (
        "Alegría que no depende de las circunstancias del momento",
        "El salmista no dice que la alegría esté en lo que está pasando "
        "ahora, dice que está «con tu rostro»: en la cercanía con Dios, no en "
        "la situación externa. Es una fuente de gozo que no sube y baja con "
        "el día que se está teniendo. Vale la pena, en un día "
        "particularmente gris, recordar que la alegría prometida aquí no "
        "depende de que el día mejore primero.",
        ["gozo", "esperanza"],
    ),
    "Salmos 19:1": (
        "Una prueba que no necesita palabras",
        "El salmo dice que los cielos «cuentan» la gloria de Dios sin usar "
        "ninguna palabra, el versículo siguiente aclara que no hay lenguaje "
        "ni idioma donde no se oiga esa voz. Es una forma de hablar de la fe "
        "que no depende de un argumento verbal: basta con mirar hacia arriba. "
        "En un día ocupado, alzar la vista un momento puede ser, en sí "
        "mismo, una forma breve de oración.",
        ["gratitud"],
    ),
    "Salmos 25:4-5": (
        "Pedir que te enseñen, no fingir que ya sabes",
        "El salmista no llega a Dios con un plan armado pidiendo aprobación, "
        "llega pidiendo que le muestren el camino, que lo encaminen. Es una "
        "postura de aprendizaje, no de certeza. «En ti he esperado todo el "
        "día» no describe una espera pasiva, describe una espera activa, "
        "dirigida a alguien concreto. Si hoy no tienes claridad sobre qué "
        "hacer, esta oración no exige que la tengas antes de orar.",
        ["duda", "esperanza"],
    ),
    "Salmos 30:5": (
        "El llanto tiene noche, pero no se queda para siempre",
        "El salmo no minimiza el llanto, le da su lugar, «por la tarde», "
        "pero le pone un límite: a la mañana vendrá la alegría. No es una "
        "promesa de que el dolor desaparecerá en segundos, es una promesa de "
        "que no es permanente. Si hoy estás en la parte de la noche de esta "
        "imagen, este versículo no te apura a salir de ahí, pero sí te "
        "recuerda que no es el final de la historia.",
        ["tristeza", "esperanza"],
    ),
    "Salmos 32:8": (
        "Dios enseña el camino, no solo lo señala de lejos",
        "La promesa no es de un mapa entregado a distancia, es de "
        "instrucción cercana, con los ojos de Dios fijos en quien camina. Es "
        "una imagen de acompañamiento activo, no de indicaciones dadas una "
        "sola vez. Si hoy sientes que necesitas más que un consejo puntual, "
        "esta promesa habla de una guía sostenida en el tiempo, no de una "
        "respuesta única.",
        ["duda", "ansiedad"],
    ),
    "Salmos 34:8": (
        "Probar antes de estar convencido del todo",
        "El salmo invita a «gustar y ver», no a estar convencido primero y "
        "después acercarse. Es una fe que se experimenta, no solo se "
        "argumenta. Dichoso, dice, el que confía, no el que ya tiene "
        "resuelta cada pregunta antes de hacerlo. Si te cuesta la certeza, "
        "este versículo no te la exige como condición previa.",
        ["gratitud", "duda"],
    ),
    "Salmos 37:4": (
        "Deleitarse primero, no negociar los deseos primero",
        "El versículo no dice que hay que reprimir los deseos del corazón "
        "para agradar a Dios, dice que, al deleitarse en Él, esos deseos se "
        "van formando de otra manera. No es una fórmula mágica para "
        "conseguir lo que se quiere, es una promesa sobre cómo cambia lo que "
        "se desea cuando el centro de la vida está en el lugar correcto.",
        ["gozo", "esperanza"],
    ),
    "Salmos 55:22": (
        "Una carga que se puede soltar, no solo compartir",
        "«Echa» es una palabra fuerte, de soltar con intención, no de "
        "simplemente mencionar el peso de pasada. La promesa que sigue, que "
        "Él te sustentará, no dice que la carga desaparecerá, dice que no "
        "tendrás que sostenerla solo. Si hoy cargas con algo que se siente "
        "demasiado pesado, este versículo no pide que lo resuelvas, pide que "
        "lo entregues.",
        ["ansiedad", "agotamiento"],
    ),
    "Salmos 62:1-2": (
        "Un alma callada, no una resignada",
        "«Callada» aquí no describe pasividad ni derrota, describe quietud "
        "confiada: el salmista dice que de Dios viene su salud, su refugio, "
        "y por eso «no resbalaré mucho». Es una calma que viene de saber en "
        "quién se apoya, no de que no haya nada que temer. Vale la pena, en "
        "medio del ruido de un día difícil, buscar esa clase de silencio "
        "interior.",
        ["paz", "fortaleza"],
    ),
    "Salmos 90:12": (
        "Contar los días para vivirlos con atención, no con miedo",
        "Pedir que se nos enseñe a «contar nuestros días» no es una "
        "invitación a la ansiedad por el tiempo que pasa, es un pedido de "
        "sabiduría para no vivirlos sin darles importancia. Es fácil dejar "
        "que los días se acumulen sin notarlos. Este salmo pide lo "
        "contrario: atención, no urgencia.",
        ["gratitud", "duelo"],
    ),
    "Salmos 107:1": (
        "Una razón que no cambia con las circunstancias",
        "El llamado a alabar no está condicionado a que las cosas vayan "
        "bien, está fundado en que Jehová es bueno y su misericordia es "
        "constante, «para siempre». Es una gratitud que no depende del día "
        "que se está teniendo, sino de algo que no cambia con él. Hoy, "
        "aunque el día no sea el mejor, esa razón sigue siendo verdad.",
        ["gratitud"],
    ),
    "Salmos 119:105": (
        "Suficiente luz para el próximo paso, no para todo el camino",
        "Una lámpara a los pies no ilumina el horizonte completo, ilumina lo "
        "justo para no tropezar ahora. Es una imagen distinta a la de tener "
        "toda la ruta iluminada de antemano. Si no tienes claridad sobre el "
        "futuro lejano, este versículo no promete esa clase de luz, promete "
        "la que hace falta para dar el siguiente paso.",
        ["duda"],
    ),
    "Salmos 147:3": (
        "Sana y venda, las dos cosas",
        "El salmo no solo dice que Dios sana a los quebrantados de corazón, "
        "agrega que liga sus heridas: una imagen de cuidado activo y "
        "detallado, no de una sanidad instantánea y distante. Las heridas "
        "emocionales muchas veces necesitan ese tipo de atención progresiva. "
        "Si tu corazón está quebrantado hoy, este versículo no promete que "
        "se resuelva de golpe, promete que se atiende con cuidado.",
        ["tristeza", "duelo"],
    ),
    "Isaías 26:3": (
        "Paz completa, condicionada a dónde se fija el pensamiento",
        "La promesa es concreta: paz completa para quien mantiene su "
        "pensamiento en Dios. No es automática ni ajena a lo que uno hace con "
        "su mente, hay una dirección de la atención que se pide sostener. "
        "Cuando la ansiedad da vueltas sobre lo mismo, este versículo no pide "
        "dejar de pensar, pide redirigir hacia dónde se piensa.",
        ["paz", "ansiedad"],
    ),
    "Isaías 30:15": (
        "La fortaleza ofrecida, y la que se prefirió en su lugar",
        "Dios ofrece descanso, quietud y confianza como camino de "
        "salvación, y el versículo termina en un giro incómodo: «y no "
        "quisisteis». El pueblo prefirió otra cosa, probablemente más "
        "activa, más controlable. Es un recordatorio de que a veces "
        "rechazamos el descanso que se nos ofrece porque no se siente como "
        "una solución suficiente. Vale la pena preguntarse si hoy también se "
        "está prefiriendo el control por sobre el reposo que se ofrece.",
        ["ansiedad", "duda"],
    ),
    "Isaías 43:2": (
        "No evita el agua ni el fuego, promete atravesarlos contigo",
        "La promesa no es que el río o el fuego no aparecerán en el camino, "
        "es que, cuando aparezcan, no estarás solo en ellos. Es una fe "
        "realista sobre las dificultades: no las niega, promete compañía en "
        "medio de ellas. Si hoy atraviesas algo que se siente como agua "
        "profunda o fuego, este versículo no pide que finjas que no arde.",
        ["ansiedad", "fortaleza"],
    ),
    "Isaías 53:5": (
        "Curados por la herida de otro",
        "Este versículo describe un intercambio: el castigo cayó sobre él, "
        "y la curación llegó a nosotros por su llaga. Es una lógica que "
        "invierte lo esperado, no es que él nos enseñe a sanar, es que su "
        "propio dolor se convierte en el medio de la sanidad ajena. Vale la "
        "pena detenerse en esa idea, no como una fórmula abstracta, sino "
        "como el fundamento concreto de por qué se puede tener esperanza "
        "incluso en el dolor.",
        ["duelo", "esperanza"],
    ),
    "Isaías 55:8-9": (
        "No entender no significa que no haya lógica",
        "Dios no dice que sus caminos sean irracionales, dice que están más "
        "allá de los nuestros, tan lejos como el cielo de la tierra. Es una "
        "distinción importante: no entender algo no es lo mismo que decir "
        "que no tiene sentido. Cuando algo en la vida no se explica con la "
        "lógica disponible, este versículo no pide resignación, pide confiar "
        "en que hay una lógica mayor que todavía no se alcanza a ver.",
        ["duda"],
    ),
    "Isaías 61:1": (
        "Buenas nuevas dirigidas específicamente a los abatidos",
        "Esta misión no se anuncia de forma genérica, se dirige a los "
        "abatidos, a los quebrantados de corazón, a los cautivos. No es un "
        "mensaje para quien ya está bien, es un mensaje pensado para quien "
        "está mal. Si hoy te sientes en esa categoría, este versículo no "
        "habla de otra persona, habla directamente de a quién estaba "
        "destinado desde el principio.",
        ["tristeza", "esperanza"],
    ),
    "Jeremías 17:7-8": (
        "Raíces profundas no evitan el calor, lo resisten",
        "El árbol junto a la corriente sigue existiendo en un año de "
        "sequía, el versículo no promete que el calor no llegará, promete "
        "que la raíz alcanza el agua incluso cuando la superficie se seca. "
        "Confiar en Jehová no evita las temporadas difíciles, da algo de "
        "dónde sostenerse mientras duran. Si este es un año de sequía para "
        "ti, esta imagen no niega el calor, promete que la raíz sigue firme.",
        ["fortaleza", "esperanza"],
    ),
    "Ezequiel 36:26": (
        "Un corazón nuevo, no una reparación del anterior",
        "La promesa no es de arreglar el corazón de piedra, es de "
        "reemplazarlo por uno de carne: una transformación completa, no un "
        "ajuste parcial. Si sientes que alguna parte de ti se endureció con "
        "el tiempo, este versículo no ofrece un remiendo, ofrece la "
        "posibilidad de algo genuinamente nuevo.",
        ["esperanza", "duda"],
    ),
    "Daniel 3:17-18": (
        "Fe que no depende del resultado esperado",
        "Los tres jóvenes declaran que Dios puede librarlos del horno, y en "
        "la misma frase agregan que, aunque no lo haga, de todos modos no "
        "van a ceder. Es una fe que no está condicionada al desenlace que "
        "ellos prefieren. Confiar no siempre significa estar seguro de cómo "
        "van a salir las cosas; a veces significa sostenerse incluso sin esa "
        "garantía.",
        ["fortaleza", "duda"],
    ),
    "Miqueas 6:8": (
        "Lo que se pide no es complicado de entender, sí de vivir",
        "El profeta resume lo que Dios pide en tres cosas concretas: "
        "justicia, misericordia y humildad. No hace falta un sistema "
        "teológico elaborado para entenderlo, la dificultad no está en "
        "comprenderlo, está en sostenerlo día a día. Vale la pena, de vez en "
        "cuando, medir la propia vida no por lo complicado que suena la fe, "
        "sino por estas tres cosas simples.",
        ["duda"],
    ),
    "Sofonías 3:17": (
        "Dios que se regocija, no solo que es regocijado",
        "La imagen no es solo de un Dios que espera nuestra alabanza, es de "
        "un Dios que se goza activamente por su pueblo, que «callará de "
        "amor» y se regocija con cantar. Es una idea poco común: no solo se "
        "nos pide alegrarnos en Dios, se describe a Dios alegrándose en "
        "nosotros. Vale la pena sentarse un momento con esa idea, no como "
        "una exigencia más, sino como una ternura inesperada.",
        ["gozo", "gratitud"],
    ),
    "Mateo 5:4": (
        "Bienaventurados los que lloran, no los que fingen no llorar",
        "Es una de las bienaventuranzas más contraintuitivas: llamar "
        "bendecidos a quienes están de duelo. No es que el llanto en sí sea "
        "deseable, es que no queda excluido de la bendición, al contrario, "
        "se le promete consuelo. Si hoy estás llorando algo real, este "
        "versículo no te pide que lo escondas para merecer una bendición.",
        ["tristeza", "duelo"],
    ),
    "Mateo 18:20": (
        "No hace falta una multitud para que Él esté presente",
        "La promesa no exige una gran congregación, dos o tres reunidos en "
        "su nombre alcanzan. Es una idea que quita presión a la idea de que "
        "la fe compartida necesita escala para tener valor. Una conversación "
        "honesta, una oración compartida entre pocos, ya cuenta como un "
        "lugar donde Él está presente.",
        ["paz", "esperanza"],
    ),
    "Mateo 7:7": (
        "Pedir, buscar, llamar: tres verbos, no uno solo",
        "La promesa no se limita a pedir una vez y recibir de inmediato, "
        "incluye buscar y llamar, verbos que sugieren persistencia, no un "
        "solo intento. No es que Dios sea difícil de alcanzar, es que a "
        "veces el camino hacia la respuesta incluye más de un paso. Si tu "
        "oración de hoy no fue respondida ayer, este versículo no la da por "
        "perdida.",
        ["esperanza", "duda"],
    ),
    "Mateo 19:26": (
        "Imposible para los hombres, no para Dios",
        "Jesús no minimiza lo difícil que parece la situación que están "
        "discutiendo, confirma que, humanamente, es imposible. El giro está "
        "después: para Dios, todo es posible. No es una negación de la "
        "dificultad real, es una ampliación de quién está involucrado en "
        "resolverla. Si algo hoy se siente imposible, este versículo no te "
        "dice que no lo es, te dice que no dependes solo de ti para "
        "resolverlo.",
        ["esperanza", "duda"],
    ),
    "Mateo 28:20": (
        "Todos los días, no solo los días difíciles",
        "La promesa de compañía no está reservada para las crisis, cubre "
        "«todos los días», incluidos los ordinarios, los aburridos, los que "
        "pasan sin pena ni gloria. Es fácil pensar en la presencia de Dios "
        "como algo que se necesita solo en emergencias. Este versículo la "
        "extiende a lo cotidiano también.",
        ["esperanza", "paz"],
    ),
    "Marcos 9:23": (
        "El límite no está en lo que Dios puede, está en si se cree",
        "El padre de este pasaje pide ayuda con una frase honesta: «si "
        "puedes algo». Jesús responde corrigiendo el condicional: la "
        "pregunta no es si él puede, es si el padre puede creer. Es una "
        "respuesta que no minimiza la duda del hombre, de hecho, el padre "
        "responde con otra frase honesta: «creo, ayuda mi incredulidad». No "
        "hace falta tener fe perfecta para pedir ayuda con la fe que falta.",
        ["duda", "fortaleza"],
    ),
    "Marcos 10:27": (
        "Lo imposible para el hombre no es la última palabra",
        "El contexto es una conversación sobre la salvación, que los "
        "discípulos consideran imposible de alcanzar por esfuerzo propio. "
        "Jesús no los contradice sobre eso, confirma que para el hombre es "
        "imposible, pero agrega que para Dios no lo es. Es un alivio "
        "distinto al de «esfuérzate más»: es la certeza de que lo que no se "
        "puede lograr solo, no depende únicamente de uno mismo.",
        ["esperanza", "duda"],
    ),
    "Marcos 11:24": (
        "Pedir con la certeza puesta en quien escucha, no en el resultado",
        "El versículo no promete que cualquier petición se cumplirá tal "
        "como se imagina, habla de una confianza puesta en Dios al orar, no "
        "de una fórmula garantizada. Es fácil leer esto como una promesa "
        "mecánica; vale más leerlo como una invitación a orar con la misma "
        "seriedad con la que se espera una respuesta real, no como un "
        "trámite.",
        ["esperanza", "duda"],
    ),
    "Lucas 1:37": (
        "Dicho a alguien enfrentando lo que parecía imposible",
        "Esta frase se le dice a María ante un anuncio que desafiaba toda "
        "lógica: un embarazo imposible según lo que ella sabía de sí misma. "
        "No es una frase genérica sobre el poder de Dios en abstracto, es "
        "una respuesta concreta a una situación que parecía no tener salida. "
        "Si hoy algo en tu vida se siente igual de imposible, esta frase "
        "nació precisamente para ese tipo de situación.",
        ["duda", "esperanza"],
    ),
    "Lucas 6:38": (
        "La medida que se da vuelve, no se pierde",
        "La imagen no es de dar y esperar una recompensa calculada, es de "
        "una generosidad que, con el tiempo, regresa de alguna forma, "
        "«apretada, remecida, y rebosando». No es una transacción inmediata, "
        "es una promesa sobre el tipo de vida que genera dar sin llevar la "
        "cuenta. Vale la pena preguntarse, hoy, si se está dando desde el "
        "temor a que falte, o desde esta confianza.",
        ["gratitud"],
    ),
    "Lucas 15:20": (
        "El padre corre antes de escuchar la disculpa",
        "En la parábola del hijo pródigo, el padre ve a su hijo «aun lejos» "
        "y corre hacia él antes de que termine de acercarse, antes de "
        "escuchar ninguna explicación. No espera el arrepentimiento perfecto "
        "para actuar con misericordia, se mueve primero. Si hoy sientes que "
        "necesitas tener todo resuelto antes de volver a algo o alguien, "
        "esta imagen sugiere otra cosa: a veces basta con empezar a caminar "
        "de regreso.",
        ["esperanza", "gozo"],
    ),
    "Lucas 18:1": (
        "Orar siempre, sobre todo cuando dan ganas de dejar de hacerlo",
        "Jesús cuenta esta parábola específicamente para enseñar a no "
        "desmayar en la oración, lo cual implica que desmayar, cansarse de "
        "orar, es algo que efectivamente sucede. No es una falla espiritual "
        "poco común, es lo suficientemente frecuente como para necesitar una "
        "parábola entera sobre el tema. Si tu oración se siente agotada "
        "últimamente, no eres el primero al que le pasa.",
        ["agotamiento", "esperanza"],
    ),
    "Juan 1:12": (
        "Una potestad recibida, no ganada",
        "El versículo no describe a alguien que se convierte en hijo de "
        "Dios por mérito propio, describe una potestad dada a quienes "
        "reciben y creen. Es un don, no un logro. Si alguna vez sentiste que "
        "la identidad como hijo de Dios había que ganársela con suficiente "
        "buen comportamiento, este versículo la describe distinto: se "
        "recibe, no se conquista.",
        ["esperanza", "duda"],
    ),
    "Juan 8:12": (
        "Seguir la luz no elimina la oscuridad alrededor",
        "La promesa no es que la oscuridad desaparecerá del mundo, es que "
        "quien sigue a Jesús no tendrá que andar en ella. Es una diferencia "
        "importante: la oscuridad puede seguir estando presente afuera, pero "
        "no define el camino de quien tiene esa luz. Si hoy el entorno se "
        "siente oscuro, este versículo habla de un tipo de claridad que no "
        "depende de que cambie el paisaje.",
        ["duda", "esperanza"],
    ),
    "Juan 10:10": (
        "Vida en abundancia, no solo vida que sobrevive",
        "Jesús contrasta su propósito con el del ladrón que solo destruye, "
        "y no dice simplemente que vino a dar vida, agrega «en abundancia». "
        "No es una promesa de supervivencia mínima, es una promesa de "
        "plenitud. Vale la pena preguntarse si la vida que se está viviendo "
        "hoy se parece más a sobrevivir o a esa abundancia prometida.",
        ["gozo", "esperanza"],
    ),
    "Juan 16:33": (
        "Paz en medio de la aflicción, no después de ella",
        "Jesús no promete una vida sin aflicción, la da por segura: «en el "
        "mundo tendréis aflicción». Lo que ofrece es paz dentro de esa "
        "realidad, no como sustituto de ella. Y agrega una razón para "
        "confiar: él ya venció al mundo. Si hoy atraviesas dificultad real, "
        "este versículo no la niega, ofrece algo para sostenerse en medio de "
        "ella.",
        ["paz", "ansiedad"],
    ),
    "Hechos 1:8": (
        "El testimonio empieza cerca antes de llegar lejos",
        "La instrucción de Jesús traza un mapa que empieza en Jerusalén, lo "
        "más cercano, lo más conocido, antes de extenderse a lo último de la "
        "tierra. No hace falta ir lejos para empezar a vivir la fe de forma "
        "visible; muchas veces el primer testimonio es el que se da en el "
        "propio entorno cotidiano.",
        ["fortaleza"],
    ),
    "Hechos 4:12": (
        "Un solo nombre, no una lista de opciones",
        "La declaración es exclusiva de forma deliberada: no hay otro "
        "nombre dado para la salvación. En una época que valora tener "
        "múltiples caminos válidos hacia cualquier meta, esta afirmación "
        "resulta particularmente directa. No busca ser diplomática, busca "
        "ser clara sobre dónde está puesta la esperanza cristiana.",
        ["esperanza"],
    ),
    "Romanos 5:8": (
        "Amados antes de merecerlo, no después",
        "El versículo es específico sobre el momento: Cristo murió por "
        "nosotros «siendo aún pecadores», no después de que nos hubiéramos "
        "corregido. El amor no esperó a que hubiera algo que lo justificara. "
        "Es una base distinta para pensar el propio valor: no se trata de "
        "haber sido suficientemente buenos, se trata de haber sido amados "
        "primero, sin condiciones previas.",
        ["gratitud", "esperanza"],
    ),
    "Romanos 8:1": (
        "Ninguna condenación, no ninguna corrección",
        "El versículo no dice que en Cristo ya no habrá corrección o "
        "disciplina, dice que no hay condenación, que es distinto: la "
        "condenación busca destruir, la corrección busca formar. Si cargas "
        "con una sensación constante de estar condenado por tus errores, "
        "este versículo distingue algo importante: la culpa que señala un "
        "error real no es lo mismo que la condena que no deja salida.",
        ["duda", "paz"],
    ),
    "Romanos 8:38-39": (
        "Una lista deliberadamente larga de lo que no puede separar",
        "Pablo no se conforma con decir «nada nos separará del amor de "
        "Dios», enumera muerte, vida, ángeles, potestades, lo presente, lo "
        "por venir, lo alto, lo bajo, como si quisiera cerrar cualquier "
        "excepción posible. Es una forma de insistencia: no hay categoría, "
        "visible o invisible, capaz de romper ese vínculo. Si hoy temes que "
        "algo específico te haya alejado de ese amor, esta lista fue "
        "escrita, en parte, para esa preocupación exacta.",
        ["ansiedad", "esperanza"],
    ),
    "Romanos 10:9": (
        "Simple de decir, no simple de vivir",
        "La fórmula que da Pablo, confesar con la boca, creer en el "
        "corazón, suena breve, casi sencilla. Pero detrás de esas dos "
        "acciones hay una vida entera de sostener esa confesión y esa "
        "creencia día tras día. No es que la salvación sea complicada de "
        "recibir; es que vivir desde ella, con el tiempo, pide más que un "
        "solo momento.",
        ["esperanza"],
    ),
    "1 Corintios 10:13": (
        "Una salida prometida, no la ausencia de tentación",
        "El versículo no promete que la tentación no llegará, promete un "
        "límite a su intensidad y una salida disponible cuando llegue. Es "
        "una promesa realista, no una fantasía de inmunidad. Si hoy sientes "
        "que algo te supera, este versículo no niega la dificultad, asegura "
        "que hay una puerta de salida, aunque todavía no se vea con "
        "claridad.",
        ["ansiedad", "fortaleza"],
    ),
    "1 Corintios 15:58": (
        "El trabajo no es en vano, aunque no se vea el fruto todavía",
        "Pablo pide firmeza y constancia con una razón concreta: el trabajo "
        "hecho en el Señor no es en vano, aunque el resultado no sea "
        "inmediato ni visible. Es un aliento para quien se siente cansado de "
        "esforzarse sin ver cambios claros. La promesa no es que el "
        "esfuerzo dará frutos mañana, es que, tarde o temprano, no habrá "
        "sido en vano.",
        ["agotamiento", "esperanza"],
    ),
    "1 Corintios 16:14": (
        "Una sola instrucción para todo lo demás",
        "Pablo cierra la carta con algo simple: que todo se haga con "
        "caridad, con amor. No es una lista larga de reglas, es un solo "
        "criterio que puede aplicarse a cualquier decisión del día. Antes de "
        "actuar hoy, esta frase ofrece una pregunta breve y útil: ¿esto se "
        "está haciendo con amor?",
        ["gratitud"],
    ),
    "2 Corintios 4:16-18": (
        "Lo que se ve es temporal, lo que no se ve es eterno",
        "Pablo no niega que el «hombre exterior» se va desgastando, lo "
        "reconoce abiertamente, pero pone el peso en lo que se renueva por "
        "dentro, día a día. Lo que hoy se siente pesado y visible, dice, es "
        "momentáneo comparado con lo que no se ve todavía. No es una "
        "negación del cansancio real, es una forma de mirarlo desde una "
        "escala más larga.",
        ["agotamiento", "esperanza"],
    ),
    "2 Corintios 12:9": (
        "La gracia se perfecciona en la debilidad, no a pesar de ella",
        "Pablo pidió tres veces que le quitaran algo que lo debilitaba, y la "
        "respuesta no fue quitarlo, fue una promesa: la gracia basta, y el "
        "poder se perfecciona en la flaqueza. No es que la debilidad sea "
        "deseable en sí misma, es que no es un obstáculo para que la gracia "
        "actúe, de hecho, ahí es donde más se nota.",
        ["duda", "fortaleza"],
    ),
    "Gálatas 2:20": (
        "Vivir desde ser amado, no desde tener que ganárselo",
        "Pablo describe una identidad completamente reconfigurada: ya no "
        "vive él, vive Cristo en él, y la vida que sigue viviendo en la "
        "carne la vive «en la fe del Hijo de Dios, el cual me amó». El "
        "motivo detrás de esta nueva forma de vivir no es el esfuerzo, es "
        "haber sido amado primero. Vale la pena notar el orden: el amor "
        "viene antes que la transformación, no después.",
        ["esperanza", "duda"],
    ),
    "Gálatas 6:9": (
        "El cansancio de hacer el bien es real, no una señal de fracaso",
        "Pablo no da por sentado que hacer el bien sea fácil de sostener, "
        "reconoce el riesgo real de cansarse y de desmayar. La promesa no es "
        "que no habrá cansancio, es que, a su tiempo, habrá cosecha si no se "
        "abandona antes. Si hoy sientes que ya no tienes fuerzas para "
        "seguir haciendo lo correcto, este versículo no minimiza ese "
        "cansancio, lo nombra directamente.",
        ["agotamiento", "esperanza"],
    ),
    "Efesios 2:10": (
        "Hechura suya, no un proyecto propio",
        "El versículo describe algo hecho por Dios, «hechura suya», con un "
        "propósito ya preparado de antemano: buenas obras para andar en "
        "ellas. No es que uno se construye a sí mismo y luego decide hacer "
        "el bien; es que ya fue creado con ese propósito incluido. Puede "
        "aliviar pensar que no hay que inventar el sentido de la propia vida "
        "desde cero.",
        ["gratitud", "duda"],
    ),
    "Efesios 3:20": (
        "Más de lo que se pide, no menos",
        "Pablo describe a Dios como capaz de hacer «mucho más "
        "abundantemente» de lo que pedimos o incluso entendemos. Es fácil "
        "orar con expectativas pequeñas, casi conformándose de antemano. "
        "Este versículo invita a lo contrario: no achicar la oración por "
        "miedo a pedir demasiado, porque la capacidad de Dios no tiene ese "
        "límite.",
        ["esperanza", "duda"],
    ),
    "Efesios 4:32": (
        "Perdonar desde haber sido perdonado, no desde el mérito ajeno",
        "El fundamento para perdonar a otros no es que lo merezcan, es que "
        "Dios ya perdonó de esa misma manera. Es una lógica distinta a la de "
        "esperar que la otra persona se disculpe lo suficiente. Si hoy te "
        "cuesta perdonar a alguien, este versículo no pregunta si esa "
        "persona se lo ganó, pregunta si tú ya recibiste ese mismo perdón "
        "antes.",
        ["gratitud"],
    ),
    "Filipenses 1:6": (
        "Una obra empezada que se promete terminar",
        "Pablo no dice que la buena obra en los filipenses ya está "
        "completa, dice que el que la comenzó la va a perfeccionar, con el "
        "tiempo, hasta el final. Es una promesa de proceso, no de "
        "perfección inmediata. Si sientes que todavía te falta mucho para "
        "ser quien deberías, este versículo no te pide llegar ya, te "
        "asegura que la obra sigue en marcha.",
        ["esperanza", "duda"],
    ),
    "Filipenses 4:4": (
        "Gozaos siempre, insistido dos veces",
        "Pablo no lo dice una sola vez, lo repite: «otra vez digo, que os "
        "gocéis», como si supiera que la primera instrucción no bastaría "
        "para convencer a alguien atravesando dificultad. No es un gozo "
        "condicionado a que todo vaya bien, es un gozo que se sostiene «en "
        "el Señor», en cualquier circunstancia.",
        ["gozo"],
    ),
    "Colosenses 3:23": (
        "Trabajar para el Señor cambia el sentido del trabajo, no la carga",
        "El versículo no promete que el trabajo será liviano, pide hacerlo "
        "de ánimo, como para el Señor y no para los hombres. Es un cambio de "
        "para quién se trabaja, más que de cuánto pesa la tarea. En un día "
        "donde el trabajo se siente sin sentido, esta frase ofrece otra "
        "forma de mirarlo, no menos esfuerzo, pero sí otro propósito detrás "
        "de él.",
        ["agotamiento", "fortaleza"],
    ),
    "1 Tesalonicenses 5:16-18": (
        "Tres instrucciones cortas para sostener siempre",
        "Gozo, oración y gratitud, «siempre», «sin cesar», «en todo», no "
        "como sentimientos que aparecen solos, sino como prácticas que se "
        "sostienen incluso cuando no vienen naturalmente. Pablo aclara que "
        "esto es «la voluntad de Dios para con vosotros», no una sugerencia "
        "opcional. No hace falta sentir gozo para empezar a practicarlo; a "
        "veces la práctica ayuda a que el sentimiento llegue después.",
        ["gozo", "gratitud"],
    ),
    "2 Timoteo 1:7": (
        "El temor no viene de Dios, entonces ¿de dónde?",
        "El versículo es claro sobre el origen: el espíritu de temor no es "
        "un regalo de Dios, lo que Él da es fortaleza, amor y templanza. Es "
        "útil, cuando el miedo aparece, hacerse esa pregunta: ¿de dónde "
        "viene esto que estoy sintiendo? No para negarlo, sino para no "
        "confundirlo con algo que Dios puso ahí.",
        ["ansiedad", "fortaleza"],
    ),
    "Hebreos 4:16": (
        "Acercarse con confianza, no con miedo a ser rechazado",
        "La invitación es a llegar «confiadamente» al trono de la gracia, "
        "no con temor de ser recibido con dureza. El propósito de acercarse "
        "no es ser juzgado, es alcanzar misericordia y ayuda oportuna. Si "
        "algo te hace dudar en acercarte a Dios hoy, este versículo describe "
        "el trono al que te acercas de otra manera: uno de gracia, no de "
        "condena.",
        ["ansiedad", "esperanza"],
    ),
    "Santiago 1:5": (
        "Pedir sabiduría sin ser reprochado por no tenerla",
        "Santiago no condiciona la respuesta a que la falta de sabiduría "
        "sea poca o justificable, dice que Dios da «a todos abundantemente, "
        "y no zahiere», sin reprochar. Es un permiso claro para admitir que "
        "no se sabe qué hacer y pedir ayuda sin vergüenza. Si hoy no tienes "
        "claridad sobre una decisión, este versículo no espera que finjas "
        "tenerla antes de orar.",
        ["duda"],
    ),
    "Santiago 1:19": (
        "Un orden concreto: oír, después hablar, después airarse",
        "Santiago no dice simplemente «cuídate al hablar», da un orden "
        "específico: pronto para oír, tardío para hablar, tardío para "
        "airarse. Es una secuencia práctica, casi mecánica, útil para "
        "momentos de tensión. Antes de responder algo hoy, vale la pena "
        "notar en cuál de esos tres pasos uno realmente está.",
        ["paz"],
    ),
    "1 Pedro 1:3": (
        "Regenerados en esperanza viva, no en optimismo pasajero",
        "Pedro no describe una esperanza genérica, la llama «viva» y la ata "
        "a un hecho concreto: la resurrección de Jesucristo. No es una "
        "actitud positiva que se elige tener, es una esperanza fundada en "
        "algo que ya sucedió. Eso le da una base distinta a la de "
        "simplemente decidir ver el lado bueno de las cosas.",
        ["esperanza", "gratitud"],
    ),
    "1 Pedro 2:9": (
        "Llamado de las tinieblas, no solo perdonado en ellas",
        "El versículo describe un traslado, no solo un perdón: «llamado de "
        "las tinieblas a su luz admirable». No es que simplemente se haya "
        "limpiado algo mientras se permanecía en el mismo lugar, es un "
        "cambio de dónde se habita. Vale la pena, hoy, recordar de dónde "
        "fuiste llamado, no solo hacia dónde vas.",
        ["gratitud", "esperanza"],
    ),
    "1 Juan 1:9": (
        "Confesar, no ocultar, es lo que lleva al perdón",
        "La promesa está condicionada a algo simple pero no siempre fácil: "
        "confesar. No dice que Dios perdona automáticamente sin que medie "
        "ningún reconocimiento, dice que es fiel y justo para perdonar "
        "cuando se confiesa. No hace falta esconder el error para acercarse "
        "a Dios, al contrario, nombrarlo con honestidad es lo que abre el "
        "camino de vuelta.",
        ["duda", "gratitud"],
    ),
    "Apocalipsis 3:20": (
        "Toca a la puerta, no la derriba",
        "La imagen es de alguien que llama y espera, no que fuerza la "
        "entrada. Dios se presenta aquí pidiendo permiso para entrar, "
        "dispuesto a cenar, a compartir algo íntimo y cotidiano. No es una "
        "escena de invasión, es una de invitación paciente. Si hoy sientes "
        "que Dios está lejos, esta imagen sugiere lo contrario: está más "
        "cerca de lo que parece, esperando que se le abra.",
        ["paz", "esperanza"],
    ),
    "Apocalipsis 21:4": (
        "Un final sin lágrimas, prometido en detalle",
        "La promesa no se queda en algo vago sobre «un futuro mejor», "
        "enumera específicamente lo que ya no habrá: muerte, llanto, "
        "clamor, dolor. Es una imagen concreta, no una frase de consuelo "
        "genérica. Para quien está atravesando una pérdida real, esta "
        "promesa no minimiza el dolor de hoy, apunta a un final donde ese "
        "dolor específico ya no tendrá lugar.",
        ["duelo", "esperanza"],
    ),
}

db = SessionLocal()

created_verses = 0
created_reflections = 0
skipped_verses = 0
skipped_reflections = 0

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
        created_verses += 1
    else:
        skipped_verses += 1
    verse_by_reference[reference] = verse

db.commit()

for reference, verse in verse_by_reference.items():
    existing = db.query(Reflection).filter(Reflection.verse_id == verse.id).first()
    if existing:
        skipped_reflections += 1
        continue
    title, body, mood_tags = REFLECTIONS[reference]
    reflection = Reflection(
        verse_id=verse.id,
        title=title,
        body=body,
        status="ai_generated",
        source="ai_assisted",
        mood_tags=mood_tags,
    )
    db.add(reflection)
    created_reflections += 1

db.commit()

print(
    f"Versículos nuevos: {created_verses} (ya existían: {skipped_verses}). "
    f"Reflexiones nuevas: {created_reflections} (ya existían: {skipped_reflections})."
)
print(
    "Quedaron en status='ai_generated' -- revísalas y pásalas a 'reviewed' en "
    "el admin (/reflections). El cron de auto_schedule_verse las va a "
    "programar solo, sin necesidad de asignarles fecha a mano."
)
