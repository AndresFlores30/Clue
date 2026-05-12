"""
CLUE - Simulador de Misterio (Version con assets graficos)

Estructura esperada de archivos:
  clue.py
  imagenes/
      Tablero.png
      Coronel_Mostaza.png
      Señorita_Escarlata.png
      Profesor_Ciruela.png
      Señora_Blanco.png
      Reverendo_Verde.png

Si la carpeta o las imagenes no existen, el juego sigue funcionando
con la representacion en formas y colores como respaldo.

Ejecutar:  python clue.py
Requiere:  pygame  (pip install pygame)
"""

import os
import sys
import random
import pygame

# =============================================================
#                       INICIALIZACION
# =============================================================
pygame.init()
pygame.font.init()

ANCHO, ALTO = 1280, 800
FPS = 60
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("CLUE - Simulador de Misterio")
reloj = pygame.time.Clock()

fuente_titulo    = pygame.font.SysFont("georgia", 72, bold=True)
fuente_subtitulo = pygame.font.SysFont("georgia", 36, bold=True)
fuente_mediana   = pygame.font.SysFont("georgia", 26, bold=True)
fuente_texto     = pygame.font.SysFont("georgia", 22)
fuente_pequena   = pygame.font.SysFont("georgia", 18)
fuente_mini      = pygame.font.SysFont("georgia", 16)

# Paleta
NEGRO   = (15, 15, 25)
FONDO   = (28, 26, 38)
FONDO2  = (38, 35, 50)
PANEL   = (45, 42, 60)
PANEL2  = (55, 52, 72)
BLANCO  = (240, 240, 245)
ROJO    = (200, 60, 70)
VERDE_O = (80, 180, 100)
DORADO  = (212, 175, 55)
GRIS    = (100, 100, 110)
GRIS_CL = (160, 160, 175)
SOMBRA  = (10, 10, 18)

# =============================================================
#                       ASSETS
# =============================================================
IMG_DIR = "imagenes"

PERSONAJE_IMG = {
    "Coronel Mostaza": "Coronel_Mostaza.png",
    "Srta. Escarlata": "Señorita_Escarlata.png",
    "Prof. Ciruela":   "Profesor_Ciruela.png",
    "Sra. Blanco":     "Señora_Blanco.png",
    "Rev. Verde":      "Reverendo_Verde.png",
}

# Coordenadas relativas (fracciones x1,y1,x2,y2) de cada habitacion sobre el tablero.
LOCACIONES_COORDS = {
    "Invernadero":    (0.63, 0.07, 0.97, 0.32),
    "Salon de baile": (0.62, 0.32, 0.97, 0.66),
    "Biblioteca":     (0.26, 0.40, 0.54, 0.82),
    "Estudio":        (0.03, 0.67, 0.25, 0.93),
    "Cocina":         (0.73, 0.68, 0.97, 0.94),
}
# Habitacion ambiental (no jugable): donde se encontro el cuerpo.
VESTIBULO_COORDS = (0.04, 0.08, 0.37, 0.30)


def cargar_imagen(nombre, tamano=None):
    """Carga una imagen desde IMG_DIR. Devuelve None si falla."""
    try:
        ruta = os.path.join(IMG_DIR, nombre)
        img = pygame.image.load(ruta).convert_alpha()
        if tamano:
            img = pygame.transform.smoothscale(img, tamano)
        return img
    except Exception as e:
        print(f"[Aviso] No se pudo cargar '{nombre}': {e}")
        return None


# =============================================================
#                       DATOS DEL JUEGO
# =============================================================
PERSONAJES = [
    ("Coronel Mostaza",  "Militar retirado",     (212, 175,  55)),
    ("Srta. Escarlata",  "Actriz famosa",        (200,  50,  80)),
    ("Prof. Ciruela",    "Cientifico recluso",   (160,  90, 200)),
    ("Sra. Blanco",      "Ama de llaves",        (220, 220, 220)),
    ("Rev. Verde",       "Sacerdote del pueblo", ( 60, 160,  90)),
]
NOMBRES_P   = [p[0] for p in PERSONAJES]
PROFESION_P = {p[0]: p[1] for p in PERSONAJES}
COLOR_P     = {p[0]: p[2] for p in PERSONAJES}

ARMAS      = ["Cuchillo", "Revolver", "Cuerda", "Llave inglesa", "Candelabro"]
LOCACIONES = ["Biblioteca", "Cocina", "Salon de baile", "Estudio", "Invernadero"]

DESCR_HABITACION = {
    "Biblioteca": ("Una sala forrada de estanterias de roble. El olor a libros viejos "
                   "se mezcla con humo frio de chimenea."),
    "Cocina": ("El olor a estofado aun persiste. Cuchillos pulcramente alineados "
               "en su soporte. Una taza humea sobre la mesa."),
    "Salon de baile": ("Cristales en el suelo bajo el piano abierto. La musica del "
                       "gramofono se detuvo a mitad de cancion."),
    "Estudio": ("Papeles esparcidos sobre el escritorio. Un cajon forzado. "
                "La caja fuerte esta abierta."),
    "Invernadero": ("Plantas exoticas se inclinan en sus macetas. La humedad pesa "
                    "en el aire. Hay tierra removida bajo un helecho."),
}

OBJETOS_BASE = {
    "Biblioteca": [
        ("Diario abierto",
         "Anotaciones sobre deudas y nombres tachados con lapiz rojo.\n"
         "La ultima fecha es de ayer."),
        ("Cenicero de plata",
         "Una colilla de puro aun tibia descansa en el. Alguien estuvo\n"
         "aqui hace muy poco tiempo."),
        ("Estante secreto",
         "Detras de un libro falso encuentras una pequena llave dorada\n"
         "y un sobre vacio con el sello de Lord Boddy."),
    ],
    "Cocina": [
        ("Cazuela en el fuego",
         "Un guiso a medio comer. La cena fue interrumpida abruptamente,\n"
         "como si alguien hubiera salido de prisa."),
        ("Tabla de cortar",
         "Manchada con un liquido oscuro que aun no se seca del todo.\n"
         "Salsa de carne... o algo peor."),
        ("Cajon de cubiertos",
         "Hay un espacio vacio donde deberia haber un utensilio.\n"
         "Algo fue tomado de aqui esta noche."),
    ],
    "Salon de baile": [
        ("Copa rota",
         "Vidrios en el suelo bajo el piano. Restos de vino tinto\n"
         "manchan la alfombra persa."),
        ("Panuelo de seda",
         "Bordado con una elegante inicial: la letra E.\n"
         "Su perfume es inconfundible."),
        ("Disco rayado",
         "El gramofono quedo atascado en una sola nota chillona,\n"
         "como si alguien lo hubiera empujado."),
    ],
    "Estudio": [
        ("Caja fuerte abierta",
         "Documentos esparcidos. Faltan papeles importantes,\n"
         "tal vez los que Lord Boddy usaba para chantajear."),
        ("Pluma manchada",
         "Tinta fresca aun. Alguien escribio algo a toda prisa\n"
         "y se llevo la hoja consigo."),
        ("Carta amenazante",
         "'Si no pagas antes del amanecer, todos sabran tu secreto.'\n"
         "No esta firmada, pero la letra es elegante."),
    ],
    "Invernadero": [
        ("Tierra removida",
         "Bajo un helecho hay marcas de un objeto enterrado y luego\n"
         "retirado. Algo pesado y largo."),
        ("Pisadas humedas",
         "Grandes y pesadas, alejandose hacia la mansion.\n"
         "Botas de hombre, recientes."),
        ("Maceta volcada",
         "Una orquidea rara yace marchita junto a fragmentos de barro.\n"
         "Hubo un forcejeo aqui."),
    ],
}

ACTIVIDADES = {
    "Coronel Mostaza": [
        "limpiando mi revolver de servicio",
        "fumando un puro y revisando mapas viejos",
        "con un brandy, recordando viejas batallas",
    ],
    "Srta. Escarlata": [
        "ensayando mi monologo del segundo acto",
        "leyendo correspondencia de mis admiradores",
        "preparandome para regresar a Londres",
    ],
    "Prof. Ciruela": [
        "anotando observaciones cientificas",
        "revisando muestras de mi ultimo experimento",
        "consultando una vieja enciclopedia",
    ],
    "Sra. Blanco": [
        "preparando el menu del dia siguiente",
        "ordenando la ropa de cama de los huespedes",
        "puliendo la plata de la casa",
    ],
    "Rev. Verde": [
        "rezando mis visperas en silencio",
        "preparando el sermon del domingo",
        "leyendo las escrituras a la luz de una vela",
    ],
}

BRIEFING_TEXTO = [
    "MADRUGADA DEL 14 DE OCTUBRE",
    "",
    "Lord Eustace Boddy, dueño de la Mansion Tudor en las afueras",
    "del pueblo de Hampstead, ha sido hallado muerto.",
    "",
    "Su cuerpo fue descubierto al amanecer por la criada de cocina",
    "en el VESTIBULO PRINCIPAL, junto a la chimenea apagada.",
    "",
    "Sin embargo, las salpicaduras de sangre y los rastros de",
    "arrastre indican que el asesinato no ocurrio alli, sino en",
    "OTRA habitacion de la mansion.",
    "",
    "Cinco personas pasaban la noche bajo este techo.",
    "Una de ellas es el asesino.",
    "",
    "Tu mision, detective: averiguar QUIEN, CON QUE arma",
    "y DONDE se cometio el crimen.",
]

HISTORIAS = {
    "Coronel Mostaza": [
        "FINAL 1: EL HONOR PERDIDO", "",
        "El Coronel Mostaza, ahogado en deudas de juego,",
        "habia pedido un prestamo a Lord Boddy.",
        "Cuando este amenazo con revelar su deshonor",
        "ante el regimiento, el coronel actuo con la",
        "frialdad de un soldado en el campo de batalla.", "",
        "Su uniforme ya no oculta su crimen.",
    ],
    "Srta. Escarlata": [
        "FINAL 2: LA ESTRELLA APAGADA", "",
        "La Srta. Escarlata descubrio que Lord Boddy",
        "planeaba publicar un libro revelando su pasado",
        "y los escandalos que arruinarian su carrera.",
        "Bajo las luces del salon, decidio que el",
        "no veria el amanecer.", "",
        "Las luces de Hollywood se apagaron para Boddy.",
    ],
    "Prof. Ciruela": [
        "FINAL 3: EL EXPERIMENTO PROHIBIDO", "",
        "El Prof. Ciruela habia sido chantajeado",
        "durante años por Lord Boddy, quien conocia",
        "sus experimentos ilegales con sustancias",
        "prohibidas por la academia.", "",
        "Esa noche, la ciencia y la venganza",
        "se mezclaron en una formula final.",
    ],
    "Sra. Blanco": [
        "FINAL 4: LOS AÑOS DE SILENCIO", "",
        "La Sra. Blanco sirvio a Lord Boddy durante",
        "treinta años, soportando humillaciones y",
        "desprecios. Cuando supo que seria despedida",
        "sin pension alguna, las llaves de la casa",
        "se convirtieron en su ultima arma.", "",
        "Treinta años de silencio terminaron en un grito.",
    ],
    "Rev. Verde": [
        "FINAL 5: EL PASADO QUE NO PERDONA", "",
        "El Rev. Verde escondia un oscuro secreto",
        "bajo su sotana: una identidad robada años atras",
        "tras un asesinato olvidado en el pueblo vecino.",
        "Lord Boddy lo habia descubierto y exigia",
        "confesion publica.", "",
        "La fe del reverendo flaqueo esa noche fatal.",
    ],
}

# =============================================================
#                          UI: BOTON
# =============================================================
class Boton:
    """Boton rectangular con sombra, hover, seleccion y soporte multilinea."""
    def __init__(self, rect, texto, color=PANEL, color_hover=DORADO,
                 fuente=None, color_texto=BLANCO):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.fuente = fuente or fuente_texto
        self.color_texto = color_texto
        self.hover = False
        self.activo = True
        self.seleccionado = False

    def actualizar(self, mouse_pos):
        self.hover = self.activo and self.rect.collidepoint(mouse_pos)

    def dibujar(self, sup):
        pygame.draw.rect(sup, SOMBRA, self.rect.move(4, 4), border_radius=10)
        if not self.activo:
            col, col_t, col_borde = (35, 35, 45), GRIS, GRIS
        elif self.seleccionado:
            col, col_t, col_borde = DORADO, NEGRO, BLANCO
        elif self.hover:
            col, col_t, col_borde = self.color_hover, NEGRO, BLANCO
        else:
            col, col_t, col_borde = self.color, self.color_texto, DORADO
        pygame.draw.rect(sup, col, self.rect, border_radius=10)
        pygame.draw.rect(sup, col_borde, self.rect, 2, border_radius=10)

        if "\n" in self.texto:
            lineas = self.texto.split("\n")
            line_h = self.fuente.get_height()
            total_h = line_h * len(lineas)
            y_inicio = self.rect.centery - total_h // 2
            for i, l in enumerate(lineas):
                txt = self.fuente.render(l, True, col_t)
                r = txt.get_rect(centerx=self.rect.centerx,
                                 top=y_inicio + i*line_h)
                sup.blit(txt, r)
        else:
            txt = self.fuente.render(self.texto, True, col_t)
            sup.blit(txt, txt.get_rect(center=self.rect.center))

    def click(self, evento):
        return (self.activo
                and evento.type == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
                and self.hover)


def dibujar_fondo():
    ventana.fill(FONDO)
    for i in range(0, ANCHO, 80):
        for j in range(0, ALTO, 80):
            pygame.draw.circle(ventana, FONDO2, (i, j), 1)


def envolver_texto(texto, fuente, ancho_max):
    """Devuelve una lista de lineas que caben en ancho_max usando la fuente."""
    palabras = texto.split(" ")
    lineas, actual = [], ""
    for w in palabras:
        prueba = (actual + " " + w).strip()
        if fuente.size(prueba)[0] <= ancho_max:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = w
    if actual:
        lineas.append(actual)
    return lineas


def dibujar_avatar(sup, personaje, centro, radio):
    """Dibuja un avatar circular - usa imagen si esta disponible, si no, un circulo de color."""
    img = juego.imgs_personajes_chico.get(personaje) if 'juego' in globals() else None
    if img:
        # Crear mascara circular para la imagen
        d = radio * 2
        scaled = pygame.transform.smoothscale(img, (d, d))
        mask_surf = pygame.Surface((d, d), pygame.SRCALPHA)
        pygame.draw.circle(mask_surf, (255, 255, 255, 255), (radio, radio), radio)
        scaled.blit(mask_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        sup.blit(scaled, (centro[0] - radio, centro[1] - radio))
        pygame.draw.circle(sup, DORADO, centro, radio, 2)
    else:
        pygame.draw.circle(sup, COLOR_P[personaje], centro, radio)
        pygame.draw.circle(sup, BLANCO, centro, radio, 2)


# =============================================================
#                       LOGICA DEL JUEGO
# =============================================================
class Juego:
    def __init__(self):
        # MENU | BRIEFING | JUGANDO | HABITACION | INTERROGATORIO | ACUSANDO | FINAL
        self.estado = "MENU"
        self.mensaje = ""
        self.tiempo_msg = 0
        self.cargar_assets()
        self.iniciar_partida()
        self.crear_botones()

    # ---------- Carga de assets graficos ----------
    def cargar_assets(self):
        # Retratos de personajes en dos tamanos
        self.imgs_personajes_chico = {}
        self.imgs_personajes_mediano = {}
        self.imgs_personajes_grande = {}
        for nombre, archivo in PERSONAJE_IMG.items():
            self.imgs_personajes_chico[nombre]   = cargar_imagen(archivo, ( 75,  95))
            self.imgs_personajes_mediano[nombre] = cargar_imagen(archivo, (110, 140))
            self.imgs_personajes_grande[nombre]  = cargar_imagen(archivo, (210, 270))

        # Tablero: se escala una vez para encajar en el area del mapa
        img = cargar_imagen("Tablero.png")
        if img:
            ratio = img.get_height() / img.get_width()
            board_w = 760
            board_h = int(board_w * ratio)
            self.img_tablero = pygame.transform.smoothscale(img, (board_w, board_h))
            self.tablero_rect = pygame.Rect(20, 110, board_w, board_h)
        else:
            self.img_tablero = None
            self.tablero_rect = None

    # ---------- Inicio de partida (RANDOM) ----------
    def iniciar_partida(self):
        # 1) Solucion aleatoria
        self.sol_personaje = random.choice(NOMBRES_P)
        self.sol_arma      = random.choice(ARMAS)
        self.sol_locacion  = random.choice(LOCACIONES)

        # 2) Candidatos a pistas (elementos NO solucion)
        candidatos = []
        for p in NOMBRES_P:
            if p != self.sol_personaje:
                candidatos.append(("personaje", p))
        for a in ARMAS:
            if a != self.sol_arma:
                candidatos.append(("arma", a))
        for l in LOCACIONES:
            if l != self.sol_locacion:
                candidatos.append(("locacion", l))
        random.shuffle(candidatos)

        # 3) Asignar 1 pista a cada habitacion (evitando autorreferencia)
        self.pistas = {}
        disponibles = candidatos[:]
        for loc in LOCACIONES:
            asignada = None
            for i, p in enumerate(disponibles):
                if not (p[0] == "locacion" and p[1] == loc):
                    asignada = disponibles.pop(i)
                    break
            if asignada is None and disponibles:
                asignada = disponibles.pop(0)
            self.pistas[loc] = asignada

        # 4) Objetos por habitacion (ambientales + 1 pista)
        self.objetos = {}
        for loc in LOCACIONES:
            objs = [{"nombre": n, "desc": d, "es_pista": False}
                    for n, d in OBJETOS_BASE[loc]]
            tipo, valor = self.pistas[loc]
            if tipo == "personaje":
                obj_p = {"nombre": "Huellas en el polvo",
                         "desc": (f"Las pisadas y la disposicion de los muebles "
                                  f"confirman que {valor}\nno estuvo en esta sala "
                                  f"en toda la noche."),
                         "es_pista": True, "tipo": tipo, "valor": valor}
            elif tipo == "arma":
                obj_p = {"nombre": "Inspeccion forense",
                         "desc": (f"Tras inspeccionar cuidadosamente la sala, "
                                  f"queda claro que el arma\nusada NO fue {valor}."),
                         "es_pista": True, "tipo": tipo, "valor": valor}
            else:
                obj_p = {"nombre": "Anotacion arrugada",
                         "desc": (f"Una nota del mayordomo cae al suelo:\n"
                                  f"'El crimen no ocurrio en {valor}.'"),
                         "es_pista": True, "tipo": tipo, "valor": valor}
            objs.append(obj_p)
            random.shuffle(objs)
            self.objetos[loc] = objs

        # 5) Coartadas
        self.coartadas = {}
        for p in NOMBRES_P:
            if p == self.sol_personaje:
                hab = random.choice([h for h in LOCACIONES if h != self.sol_locacion])
            else:
                hab = random.choice(LOCACIONES)
            actividad = random.choice(ACTIVIDADES[p])
            self.coartadas[p] = (hab, actividad)

        # 6) Estado del jugador
        self.visitadas = set()
        self.descartados = {"personaje": set(), "arma": set(), "locacion": set()}
        self.objetos_examinados = set()
        self.interrogados = set()
        self.locacion_actual = None
        self.objeto_idx = None
        self.personaje_int_actual = None
        self.acu_personaje = None
        self.acu_arma = None
        self.acu_locacion = None
        self.gano = False

    # ---------- Construccion de botones ----------
    def crear_botones(self):
        # MENU
        self.btn_iniciar = Boton((ANCHO//2 - 200, 480, 400, 70),
                                 "INICIAR INVESTIGACION",
                                 color=PANEL2, fuente=fuente_mediana)
        self.btn_salir = Boton((ANCHO//2 - 100, 580, 200, 50),
                               "Salir", color=PANEL)

        # BRIEFING
        self.btn_briefing_continuar = Boton(
            (ANCHO//2 - 220, 720, 440, 60),
            "COMENZAR INVESTIGACION", color=(30, 100, 50),
            color_hover=VERDE_O, fuente=fuente_mediana)

        # JUGANDO: botones de respaldo si no hay tablero
        self.btn_locaciones = []
        for i, loc in enumerate(LOCACIONES):
            self.btn_locaciones.append(
                Boton((60, 130 + i*80, 380, 70), loc, fuente=fuente_mediana))

        # Botones de accion (panel derecho)
        self.btn_interrogar = Boton((800, 625, 460, 55),
                                    "INTERROGAR SOSPECHOSOS",
                                    color=PANEL2, color_hover=DORADO,
                                    fuente=fuente_mediana)
        self.btn_acusar = Boton((800, 690, 460, 55),
                                "HACER ACUSACION FINAL",
                                color=(120, 30, 40), color_hover=ROJO,
                                fuente=fuente_mediana)

        # HABITACION
        self.btn_volver_hab = Boton((60, 720, 200, 50),
                                    "<- Volver al mapa", color=PANEL)

        # INTERROGATORIO
        self.btn_sospechosos = []
        for i, p in enumerate(NOMBRES_P):
            txt = f"{p}\n{PROFESION_P[p]}"
            self.btn_sospechosos.append(
                Boton((60, 150 + i*100, 380, 90), txt, fuente=fuente_pequena))
        self.btn_volver_int = Boton((60, 720, 200, 50),
                                    "<- Volver al mapa", color=PANEL)

        # ACUSANDO
        self.btn_acu_p = [Boton((80,  220 + i*80, 320, 65), p, fuente=fuente_texto)
                          for i, p in enumerate(NOMBRES_P)]
        self.btn_acu_a = [Boton((480, 220 + i*80, 320, 65), a, fuente=fuente_texto)
                          for i, a in enumerate(ARMAS)]
        self.btn_acu_l = [Boton((880, 220 + i*80, 320, 65), l, fuente=fuente_texto)
                          for i, l in enumerate(LOCACIONES)]
        self.btn_confirmar = Boton((ANCHO//2 - 180, 720, 360, 60),
                                   "CONFIRMAR ACUSACION",
                                   color=(30, 100, 50), color_hover=VERDE_O,
                                   fuente=fuente_mediana)
        self.btn_volver_acu = Boton((40, 720, 180, 50),
                                    "<- Volver", color=PANEL)

        # FINAL
        self.btn_jugar_otra = Boton((ANCHO//2 - 150, 720, 300, 60),
                                    "JUGAR DE NUEVO",
                                    color=PANEL2, fuente=fuente_mediana)

    # ---------- Helpers ----------
    def get_loc_rect(self, loc_name):
        """Rect clicable sobre el tablero para la habitacion dada."""
        if not self.tablero_rect:
            return None
        x1, y1, x2, y2 = LOCACIONES_COORDS[loc_name]
        bx, by = self.tablero_rect.x, self.tablero_rect.y
        bw, bh = self.tablero_rect.w, self.tablero_rect.h
        return pygame.Rect(bx + x1*bw, by + y1*bh,
                           (x2 - x1)*bw, (y2 - y1)*bh)

    def get_vestibulo_rect(self):
        if not self.tablero_rect:
            return None
        x1, y1, x2, y2 = VESTIBULO_COORDS
        bx, by = self.tablero_rect.x, self.tablero_rect.y
        bw, bh = self.tablero_rect.w, self.tablero_rect.h
        return pygame.Rect(bx + x1*bw, by + y1*bh,
                           (x2 - x1)*bw, (y2 - y1)*bh)

    def set_mensaje(self, msg):
        self.mensaje = msg
        self.tiempo_msg = pygame.time.get_ticks()

    # ---------- Acciones ----------
    def entrar_habitacion(self, loc):
        self.locacion_actual = loc
        self.objeto_idx = None
        self.visitadas.add(loc)
        self.btn_objs = []
        for i in range(len(self.objetos[loc])):
            self.btn_objs.append(
                Boton((60, 280 + i*75, 420, 65), "", fuente=fuente_texto))
        self.estado = "HABITACION"

    def examinar_objeto(self, idx):
        self.objeto_idx = idx
        loc = self.locacion_actual
        clave = (loc, idx)
        if clave not in self.objetos_examinados:
            self.objetos_examinados.add(clave)
            obj = self.objetos[loc][idx]
            if obj.get("es_pista"):
                self.descartados[obj["tipo"]].add(obj["valor"])

    def confirmar_acusacion(self):
        self.gano = (self.acu_personaje == self.sol_personaje
                     and self.acu_arma  == self.sol_arma
                     and self.acu_locacion == self.sol_locacion)
        self.estado = "FINAL"

    # =========================================================
    #                    PANTALLA: MENU
    # =========================================================
    def dibujar_menu(self):
        dibujar_fondo()
        titulo = fuente_titulo.render("C  L  U  E", True, DORADO)
        ventana.blit(titulo, titulo.get_rect(center=(ANCHO//2, 180)))
        sub = fuente_subtitulo.render("Simulador de Misterio", True, BLANCO)
        ventana.blit(sub, sub.get_rect(center=(ANCHO//2, 260)))
        pygame.draw.line(ventana, DORADO,
                         (ANCHO//2 - 320, 310), (ANCHO//2 + 320, 310), 2)

        intro = [
            "Lord Boddy ha sido asesinado en su mansion.",
            "5 sospechosos, 5 armas, 5 habitaciones.",
            "Examina objetos, interroga a los sospechosos",
            "y descubre quien, con que y donde.",
        ]
        for i, l in enumerate(intro):
            txt = fuente_texto.render(l, True, GRIS_CL)
            ventana.blit(txt, txt.get_rect(center=(ANCHO//2, 350 + i*30)))

        self.btn_iniciar.dibujar(ventana)
        self.btn_salir.dibujar(ventana)

        cred = fuente_pequena.render(
            "Caso clasico de misterio - 5 finales posibles", True, GRIS)
        ventana.blit(cred, cred.get_rect(center=(ANCHO//2, ALTO - 30)))

    # =========================================================
    #                    PANTALLA: BRIEFING
    # =========================================================
    def dibujar_briefing(self):
        dibujar_fondo()

        t = fuente_subtitulo.render("EXPEDIENTE DEL CASO", True, DORADO)
        ventana.blit(t, t.get_rect(center=(ANCHO//2, 50)))
        pygame.draw.line(ventana, DORADO,
                         (ANCHO//2 - 380, 90), (ANCHO//2 + 380, 90), 2)

        # Texto del briefing en la izquierda
        x_text = 60
        y_t = 110
        for linea in BRIEFING_TEXTO:
            if linea == "":
                y_t += 14
                continue
            if linea == BRIEFING_TEXTO[0]:
                surf = fuente_mediana.render(linea, True, DORADO)
            else:
                surf = fuente_texto.render(linea, True, BLANCO)
            ventana.blit(surf, (x_text, y_t))
            y_t += 32

        # Panel de sospechosos a la derecha (con retratos)
        panel_x = 760
        panel_w = 480
        panel_rect = pygame.Rect(panel_x, 110, panel_w, 580)
        pygame.draw.rect(ventana, PANEL, panel_rect, border_radius=12)
        pygame.draw.rect(ventana, DORADO, panel_rect, 2, border_radius=12)
        ventana.blit(fuente_mediana.render("LOS 5 SOSPECHOSOS", True, DORADO),
                     (panel_x + 24, 125))

        for i, (nombre, prof, color) in enumerate(PERSONAJES):
            y = 165 + i * 102
            img = self.imgs_personajes_chico.get(nombre)
            if img:
                # Marco del retrato
                marco = pygame.Rect(panel_x + 20, y, 75, 95)
                pygame.draw.rect(ventana, NEGRO, marco, border_radius=4)
                ventana.blit(img, marco.topleft)
                pygame.draw.rect(ventana, DORADO, marco, 2, border_radius=4)
            else:
                pygame.draw.circle(ventana, color,
                                   (panel_x + 50, y + 47), 35)
                pygame.draw.circle(ventana, BLANCO,
                                   (panel_x + 50, y + 47), 35, 2)
            ventana.blit(fuente_texto.render(nombre, True, BLANCO),
                         (panel_x + 110, y + 22))
            ventana.blit(fuente_pequena.render(prof, True, GRIS_CL),
                         (panel_x + 110, y + 52))

        self.btn_briefing_continuar.dibujar(ventana)

    # =========================================================
    #                    PANTALLA: JUEGO PRINCIPAL
    # =========================================================
    def dibujar_juego(self):
        dibujar_fondo()
        mouse = pygame.mouse.get_pos()

        # Cabecera
        ventana.blit(fuente_subtitulo.render("Mansion Boddy", True, DORADO),
                     (20, 20))
        ventana.blit(fuente_pequena.render(
            f"Habitaciones investigadas: {len(self.visitadas)}/5    "
            f"Sospechosos interrogados: {len(self.interrogados)}/5",
            True, GRIS_CL), (20, 75))

        # ---- TABLERO ----
        if self.img_tablero:
            bx, by = self.tablero_rect.x, self.tablero_rect.y
            # Marco
            marco = self.tablero_rect.inflate(6, 6)
            pygame.draw.rect(ventana, DORADO, marco, border_radius=6)
            ventana.blit(self.img_tablero, (bx, by))

            # Vestibulo (no jugable, easter egg)
            vrect = self.get_vestibulo_rect()
            if vrect and vrect.collidepoint(mouse):
                surf = pygame.Surface(vrect.size, pygame.SRCALPHA)
                surf.fill((200, 60, 70, 70))
                ventana.blit(surf, vrect.topleft)
                pygame.draw.rect(ventana, ROJO, vrect, 3, border_radius=6)
                etiqueta = fuente_pequena.render(
                    "Aqui se hallo el cuerpo", True, BLANCO)
                fondo = pygame.Surface(
                    (etiqueta.get_width()+12, etiqueta.get_height()+6),
                    pygame.SRCALPHA)
                fondo.fill((0, 0, 0, 220))
                ventana.blit(fondo, (vrect.x + 6, vrect.bottom - 28))
                ventana.blit(etiqueta, (vrect.x + 12, vrect.bottom - 26))

            # Habitaciones jugables
            for loc_name in LOCACIONES:
                rect = self.get_loc_rect(loc_name)
                hover = rect.collidepoint(mouse)
                visitada = loc_name in self.visitadas

                if hover:
                    surf = pygame.Surface(rect.size, pygame.SRCALPHA)
                    surf.fill((212, 175, 55, 85))
                    ventana.blit(surf, rect.topleft)
                    pygame.draw.rect(ventana, DORADO, rect, 3,
                                     border_radius=8)
                elif visitada:
                    pygame.draw.rect(ventana, VERDE_O, rect, 2,
                                     border_radius=8)

                # Etiqueta con nombre del cuarto
                etiqueta_txt = loc_name
                if visitada:
                    etiqueta_txt += "  [OK]"
                etiqueta = fuente_pequena.render(etiqueta_txt, True, BLANCO)
                fondo = pygame.Surface(
                    (etiqueta.get_width()+14, etiqueta.get_height()+6),
                    pygame.SRCALPHA)
                color_fondo = ((30, 100, 50, 230) if visitada
                               else (0, 0, 0, 200))
                fondo.fill(color_fondo)
                ventana.blit(fondo, (rect.x + 6, rect.y + 6))
                ventana.blit(etiqueta, (rect.x + 13, rect.y + 9))
        else:
            # Fallback: lista de botones a la izquierda
            for i, btn in enumerate(self.btn_locaciones):
                btn.dibujar(ventana)
                if LOCACIONES[i] in self.visitadas:
                    check = fuente_pequena.render("[VISITADA]", True, VERDE_O)
                    ventana.blit(check,
                                 (btn.rect.right - check.get_width() - 12,
                                  btn.rect.bottom - 22))

        # ---- PANEL DERECHO: CUADERNO ----
        panel_x, panel_w = 800, 460
        panel_rect = pygame.Rect(panel_x, 105, panel_w, 510)
        pygame.draw.rect(ventana, PANEL, panel_rect, border_radius=12)
        pygame.draw.rect(ventana, DORADO, panel_rect, 2, border_radius=12)
        ventana.blit(fuente_mediana.render("Cuaderno del Detective",
                                           True, DORADO),
                     (panel_x + 16, 115))

        # Tres columnas: sospechosos | armas | locaciones
        col_w_s, col_w_a, col_w_l = 180, 100, 145
        gap = 8
        cx = panel_x + 16
        col_defs = [
            ("SOSPECHOSOS", NOMBRES_P, "personaje", col_w_s),
            ("ARMAS",       ARMAS,     "arma",      col_w_a),
            ("LOCACIONES",  LOCACIONES,"locacion",  col_w_l),
        ]
        for (tit, items, tipo, w) in col_defs:
            ventana.blit(fuente_pequena.render(tit, True, BLANCO), (cx, 155))
            pygame.draw.line(ventana, DORADO,
                             (cx, 180), (cx + w - 4, 180), 1)
            for i, it in enumerate(items):
                desc = it in self.descartados[tipo]
                color = GRIS if desc else BLANCO
                if tipo == "personaje":
                    main = fuente_pequena.render(it, True, color)
                    prof = fuente_mini.render(PROFESION_P[it], True, GRIS)
                    ventana.blit(main, (cx, 195 + i*52))
                    ventana.blit(prof, (cx, 215 + i*52))
                    if desc:
                        y_l = 195 + i*52 + main.get_height()//2
                        pygame.draw.line(ventana, ROJO, (cx, y_l),
                                         (cx + main.get_width(), y_l), 2)
                else:
                    txt = fuente_pequena.render(it, True, color)
                    ventana.blit(txt, (cx, 195 + i*45))
                    if desc:
                        y_l = 195 + i*45 + txt.get_height()//2
                        pygame.draw.line(ventana, ROJO, (cx, y_l),
                                         (cx + txt.get_width(), y_l), 2)
            cx += w + gap

        # Coartadas (parte baja del panel)
        if self.interrogados:
            ventana.blit(fuente_pequena.render("Coartadas:", True, DORADO),
                         (panel_x + 16, 470))
            ordenadas = sorted(self.interrogados,
                               key=lambda x: NOMBRES_P.index(x))
            for i, p in enumerate(ordenadas):
                hab, _ = self.coartadas[p]
                txt = f"- {p}: en {hab}"
                surf = fuente_mini.render(txt, True, GRIS_CL)
                ventana.blit(surf, (panel_x + 22, 495 + i*22))

        # Botones de accion
        self.btn_interrogar.dibujar(ventana)
        self.btn_acusar.dibujar(ventana)

        # Mensaje temporal (vestibulo, etc.)
        if self.mensaje and pygame.time.get_ticks() - self.tiempo_msg < 4000:
            msg_rect = pygame.Rect(20, ALTO - 50, 760, 36)
            pygame.draw.rect(ventana, (50, 30, 35), msg_rect, border_radius=8)
            pygame.draw.rect(ventana, ROJO, msg_rect, 2, border_radius=8)
            surf = fuente_pequena.render(self.mensaje, True, BLANCO)
            ventana.blit(surf, surf.get_rect(center=msg_rect.center))

    # =========================================================
    #                    PANTALLA: HABITACION
    # =========================================================
    def dibujar_habitacion(self):
        dibujar_fondo()
        loc = self.locacion_actual

        t = fuente_subtitulo.render(loc, True, DORADO)
        ventana.blit(t, (60, 30))
        pygame.draw.line(ventana, DORADO, (60, 90), (1220, 90), 2)

        descr = DESCR_HABITACION[loc]
        lineas = envolver_texto(descr, fuente_texto, 1140)
        for i, l in enumerate(lineas):
            ventana.blit(fuente_texto.render(l, True, GRIS_CL),
                         (60, 110 + i*28))

        ventana.blit(fuente_mediana.render("Objetos en la sala:",
                                           True, BLANCO), (60, 240))
        objs = self.objetos[loc]
        for i, btn in enumerate(self.btn_objs):
            obj = objs[i]
            examinado = (loc, i) in self.objetos_examinados
            seleccionado = (i == self.objeto_idx)
            prefijo = "[X] " if examinado else "[ ] "
            btn.texto = prefijo + obj["nombre"]
            btn.seleccionado = seleccionado
            btn.dibujar(ventana)

        panel_rect = pygame.Rect(520, 240, 700, 420)
        pygame.draw.rect(ventana, PANEL, panel_rect, border_radius=12)
        pygame.draw.rect(ventana, DORADO, panel_rect, 2, border_radius=12)

        if self.objeto_idx is None:
            msg = fuente_texto.render(
                "Selecciona un objeto a la izquierda para examinarlo.",
                True, GRIS_CL)
            ventana.blit(msg, msg.get_rect(center=panel_rect.center))
        else:
            obj = objs[self.objeto_idx]
            color_titulo = DORADO if obj.get("es_pista") else BLANCO
            ventana.blit(fuente_mediana.render(obj["nombre"], True, color_titulo),
                         (panel_rect.x + 20, panel_rect.y + 20))
            pygame.draw.line(ventana, DORADO,
                             (panel_rect.x + 20, panel_rect.y + 60),
                             (panel_rect.right - 20, panel_rect.y + 60), 1)
            y_t = panel_rect.y + 80
            for parr in obj["desc"].split("\n"):
                for l in envolver_texto(parr, fuente_texto,
                                          panel_rect.width - 40):
                    ventana.blit(fuente_texto.render(l, True, BLANCO),
                                 (panel_rect.x + 20, y_t))
                    y_t += 30
            if obj.get("es_pista"):
                aviso = fuente_pequena.render(
                    ">> Pista clave anadida al cuaderno <<", True, VERDE_O)
                ventana.blit(aviso,
                             (panel_rect.x + 20, panel_rect.bottom - 40))

        self.btn_volver_hab.dibujar(ventana)

    # =========================================================
    #                    PANTALLA: INTERROGATORIO
    # =========================================================
    def dibujar_interrogatorio(self):
        dibujar_fondo()
        t = fuente_subtitulo.render("Sala de Interrogatorios", True, DORADO)
        ventana.blit(t, (60, 30))
        pygame.draw.line(ventana, DORADO, (60, 90), (1220, 90), 2)
        ventana.blit(fuente_pequena.render(
            "Selecciona a un sospechoso para preguntarle donde estuvo "
            "esa noche.", True, GRIS_CL), (60, 105))

        # Botones (con avatar pequeno integrado)
        for i, btn in enumerate(self.btn_sospechosos):
            p = NOMBRES_P[i]
            btn.seleccionado = (p == self.personaje_int_actual)
            btn.dibujar(ventana)
            # Avatar pequeño al lado izquierdo del boton
            img = self.imgs_personajes_chico.get(p)
            if img:
                # Recortado a un tamaño aun mas pequeno y dentro del boton
                small = pygame.transform.smoothscale(img, (60, 76))
                ventana.blit(small,
                             (btn.rect.x + 8, btn.rect.y + 7))
            if p in self.interrogados:
                check = fuente_mini.render("[OK]", True, VERDE_O)
                ventana.blit(check,
                             (btn.rect.right - 40, btn.rect.top + 6))

        # Panel derecho con la coartada
        panel_rect = pygame.Rect(520, 150, 700, 540)
        pygame.draw.rect(ventana, PANEL, panel_rect, border_radius=12)
        pygame.draw.rect(ventana, DORADO, panel_rect, 2, border_radius=12)

        if self.personaje_int_actual is None:
            msg = fuente_texto.render(
                "Selecciona un sospechoso para escuchar su declaracion.",
                True, GRIS_CL)
            ventana.blit(msg, msg.get_rect(center=panel_rect.center))
        else:
            p = self.personaje_int_actual
            hab, actividad = self.coartadas[p]

            # Retrato grande a la izquierda del panel
            img_g = self.imgs_personajes_grande.get(p)
            if img_g:
                retrato_pos = (panel_rect.x + 20, panel_rect.y + 30)
                # Marco
                marco = pygame.Rect(retrato_pos[0]-3, retrato_pos[1]-3,
                                    img_g.get_width()+6,
                                    img_g.get_height()+6)
                pygame.draw.rect(ventana, DORADO, marco, border_radius=6)
                ventana.blit(img_g, retrato_pos)
                text_x = panel_rect.x + 250
            else:
                # Fallback: circulo de color
                cx_c, cy_c = panel_rect.x + 80, panel_rect.y + 80
                pygame.draw.circle(ventana, COLOR_P[p], (cx_c, cy_c), 50)
                pygame.draw.circle(ventana, BLANCO, (cx_c, cy_c), 50, 2)
                text_x = panel_rect.x + 160

            ventana.blit(fuente_mediana.render(p, True, BLANCO),
                         (text_x, panel_rect.y + 40))
            ventana.blit(fuente_pequena.render(PROFESION_P[p], True, GRIS_CL),
                         (text_x, panel_rect.y + 72))

            pygame.draw.line(ventana, DORADO,
                             (panel_rect.x + 20, panel_rect.y + 320),
                             (panel_rect.right - 20, panel_rect.y + 320), 1)

            ventana.blit(fuente_mediana.render("Declaracion:", True, DORADO),
                         (panel_rect.x + 20, panel_rect.y + 340))

            decl = (f'"Estuve toda la noche en {hab}, {actividad}. '
                    f'No vi nada raro hasta que el mayordomo dio la alarma."')
            lineas = envolver_texto(decl, fuente_texto,
                                     panel_rect.width - 40)
            for i, l in enumerate(lineas):
                ventana.blit(fuente_texto.render(l, True, BLANCO),
                             (panel_rect.x + 20, panel_rect.y + 385 + i*30))

            nota = fuente_pequena.render(
                "Recuerda: el culpable mentira sobre su ubicacion.",
                True, GRIS_CL)
            ventana.blit(nota,
                         (panel_rect.x + 20, panel_rect.bottom - 30))

        self.btn_volver_int.dibujar(ventana)

    # =========================================================
    #                    PANTALLA: ACUSACION
    # =========================================================
    def dibujar_acusacion(self):
        dibujar_fondo()
        t = fuente_subtitulo.render("ACUSACION FINAL", True, ROJO)
        ventana.blit(t, t.get_rect(center=(ANCHO//2, 60)))
        s = fuente_texto.render(
            "Selecciona quien, con que arma y en que lugar:", True, BLANCO)
        ventana.blit(s, s.get_rect(center=(ANCHO//2, 110)))

        for et, x in [("SOSPECHOSO", 240), ("ARMA", 640), ("LOCACION", 1040)]:
            tt = fuente_mediana.render(et, True, DORADO)
            ventana.blit(tt, tt.get_rect(center=(x, 175)))

        for i, btn in enumerate(self.btn_acu_p):
            btn.seleccionado = (NOMBRES_P[i] == self.acu_personaje)
            btn.dibujar(ventana)
        for i, btn in enumerate(self.btn_acu_a):
            btn.seleccionado = (ARMAS[i] == self.acu_arma)
            btn.dibujar(ventana)
        for i, btn in enumerate(self.btn_acu_l):
            btn.seleccionado = (LOCACIONES[i] == self.acu_locacion)
            btn.dibujar(ventana)

        listo = bool(self.acu_personaje and self.acu_arma and self.acu_locacion)
        self.btn_confirmar.activo = listo
        self.btn_confirmar.dibujar(ventana)
        self.btn_volver_acu.dibujar(ventana)

        if self.acu_personaje or self.acu_arma or self.acu_locacion:
            txt = (f"Yo acuso a {self.acu_personaje or '???'} "
                   f"con {self.acu_arma or '???'} "
                   f"en {self.acu_locacion or '???'}.")
            tt = fuente_texto.render(txt, True, DORADO)
            ventana.blit(tt, tt.get_rect(center=(ANCHO//2, 670)))

    # =========================================================
    #                    PANTALLA: FINAL
    # =========================================================
    def dibujar_final(self):
        dibujar_fondo()
        # Retrato del culpable (si hay imagen)
        img_culp = self.imgs_personajes_grande.get(self.sol_personaje)

        if self.gano:
            t = fuente_subtitulo.render("CASO RESUELTO", True, VERDE_O)
            ventana.blit(t, t.get_rect(center=(ANCHO//2, 50)))
            sub_txt = (f"{self.sol_personaje}  -  {self.sol_arma}  -  "
                       f"{self.sol_locacion}")
            sub = fuente_mediana.render(sub_txt, True, DORADO)
            ventana.blit(sub, sub.get_rect(center=(ANCHO//2, 95)))
            pygame.draw.line(ventana, DORADO,
                             (ANCHO//2 - 420, 130),
                             (ANCHO//2 + 420, 130), 2)
        else:
            t = fuente_subtitulo.render("ACUSACION ERRONEA", True, ROJO)
            ventana.blit(t, t.get_rect(center=(ANCHO//2, 50)))
            tu = (f"Acusaste a {self.acu_personaje} "
                  f"con {self.acu_arma} en {self.acu_locacion}")
            ventana.blit(fuente_texto.render(tu, True, GRIS_CL),
                         fuente_texto.render(tu, True, GRIS_CL)
                         .get_rect(center=(ANCHO//2, 95)))
            real = (f"VERDAD: {self.sol_personaje}  -  {self.sol_arma}  -  "
                    f"{self.sol_locacion}")
            ventana.blit(fuente_mediana.render(real, True, DORADO),
                         fuente_mediana.render(real, True, DORADO)
                         .get_rect(center=(ANCHO//2, 130)))
            pygame.draw.line(ventana, DORADO,
                             (ANCHO//2 - 420, 165),
                             (ANCHO//2 + 420, 165), 2)

        # Retrato del culpable a la izquierda
        if img_culp:
            r_pos = (90, 200)
            marco = pygame.Rect(r_pos[0]-4, r_pos[1]-4,
                                img_culp.get_width()+8,
                                img_culp.get_height()+8)
            pygame.draw.rect(ventana, DORADO, marco, border_radius=8)
            ventana.blit(img_culp, r_pos)
            tx = 340
        else:
            tx = 100

        # Texto de la historia a la derecha del retrato
        historia = HISTORIAS[self.sol_personaje]
        y_t = 200
        for i, linea in enumerate(historia):
            if i == 0:
                surf = fuente_mediana.render(linea, True, DORADO)
            else:
                surf = fuente_texto.render(linea, True, BLANCO)
            ventana.blit(surf, (tx, y_t))
            y_t += 36

        if not self.gano:
            cierre = fuente_texto.render(
                "El verdadero culpable escapo. Caso cerrado.", True, ROJO)
            ventana.blit(cierre, cierre.get_rect(
                center=(ANCHO//2, 670)))

        self.btn_jugar_otra.dibujar(ventana)

    # =========================================================
    #                   EVENTOS Y DESPACHADOR
    # =========================================================
    def manejar_eventos(self, eventos):
        mouse = pygame.mouse.get_pos()

        if self.estado == "MENU":
            self.btn_iniciar.actualizar(mouse)
            self.btn_salir.actualizar(mouse)
            for ev in eventos:
                if self.btn_iniciar.click(ev):
                    self.iniciar_partida()
                    self.estado = "BRIEFING"
                if self.btn_salir.click(ev):
                    return False

        elif self.estado == "BRIEFING":
            self.btn_briefing_continuar.actualizar(mouse)
            for ev in eventos:
                if self.btn_briefing_continuar.click(ev):
                    self.estado = "JUGANDO"

        elif self.estado == "JUGANDO":
            self.btn_interrogar.actualizar(mouse)
            self.btn_acusar.actualizar(mouse)
            if not self.img_tablero:
                for btn in self.btn_locaciones:
                    btn.actualizar(mouse)
            for ev in eventos:
                if (ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1
                        and self.img_tablero):
                    # Click sobre el tablero
                    for loc_name in LOCACIONES:
                        rect = self.get_loc_rect(loc_name)
                        if rect and rect.collidepoint(ev.pos):
                            self.entrar_habitacion(loc_name)
                            break
                    else:
                        # Vestibulo (easter egg)
                        vrect = self.get_vestibulo_rect()
                        if vrect and vrect.collidepoint(ev.pos):
                            self.set_mensaje(
                                "Vestibulo Principal: aqui se hallo el "
                                "cuerpo, pero el crimen ocurrio en OTRA "
                                "habitacion.")
                if not self.img_tablero:
                    for i, btn in enumerate(self.btn_locaciones):
                        if btn.click(ev):
                            self.entrar_habitacion(LOCACIONES[i])
                if self.btn_interrogar.click(ev):
                    self.personaje_int_actual = None
                    self.estado = "INTERROGATORIO"
                if self.btn_acusar.click(ev):
                    self.estado = "ACUSANDO"

        elif self.estado == "HABITACION":
            for btn in self.btn_objs:
                btn.actualizar(mouse)
            self.btn_volver_hab.actualizar(mouse)
            for ev in eventos:
                for i, btn in enumerate(self.btn_objs):
                    if btn.click(ev):
                        self.examinar_objeto(i)
                if self.btn_volver_hab.click(ev):
                    self.estado = "JUGANDO"

        elif self.estado == "INTERROGATORIO":
            for btn in self.btn_sospechosos:
                btn.actualizar(mouse)
            self.btn_volver_int.actualizar(mouse)
            for ev in eventos:
                for i, btn in enumerate(self.btn_sospechosos):
                    if btn.click(ev):
                        self.personaje_int_actual = NOMBRES_P[i]
                        self.interrogados.add(NOMBRES_P[i])
                if self.btn_volver_int.click(ev):
                    self.estado = "JUGANDO"

        elif self.estado == "ACUSANDO":
            for btn in self.btn_acu_p + self.btn_acu_a + self.btn_acu_l:
                btn.actualizar(mouse)
            self.btn_confirmar.actualizar(mouse)
            self.btn_volver_acu.actualizar(mouse)
            for ev in eventos:
                for i, btn in enumerate(self.btn_acu_p):
                    if btn.click(ev):
                        self.acu_personaje = NOMBRES_P[i]
                for i, btn in enumerate(self.btn_acu_a):
                    if btn.click(ev):
                        self.acu_arma = ARMAS[i]
                for i, btn in enumerate(self.btn_acu_l):
                    if btn.click(ev):
                        self.acu_locacion = LOCACIONES[i]
                if self.btn_confirmar.click(ev):
                    self.confirmar_acusacion()
                if self.btn_volver_acu.click(ev):
                    self.estado = "JUGANDO"

        elif self.estado == "FINAL":
            self.btn_jugar_otra.actualizar(mouse)
            for ev in eventos:
                if self.btn_jugar_otra.click(ev):
                    self.iniciar_partida()
                    self.estado = "MENU"

        return True

    def dibujar(self):
        if   self.estado == "MENU":           self.dibujar_menu()
        elif self.estado == "BRIEFING":       self.dibujar_briefing()
        elif self.estado == "JUGANDO":        self.dibujar_juego()
        elif self.estado == "HABITACION":     self.dibujar_habitacion()
        elif self.estado == "INTERROGATORIO": self.dibujar_interrogatorio()
        elif self.estado == "ACUSANDO":       self.dibujar_acusacion()
        elif self.estado == "FINAL":          self.dibujar_final()


# =============================================================
#                          MAIN LOOP
# =============================================================
def main():
    global juego
    juego = Juego()
    corriendo = True
    while corriendo:
        eventos = pygame.event.get()
        for ev in eventos:
            if ev.type == pygame.QUIT:
                corriendo = False
        if not juego.manejar_eventos(eventos):
            corriendo = False
        juego.dibujar()
        pygame.display.flip()
        reloj.tick(FPS)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()