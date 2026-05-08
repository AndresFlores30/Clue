import pygame
import random
import sys

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
NEGRO     = (15, 15, 25)
FONDO     = (28, 26, 38)
FONDO2    = (38, 35, 50)
PANEL     = (45, 42, 60)
PANEL2    = (55, 52, 72)
BLANCO    = (240, 240, 245)
ROJO      = (200, 60, 70)
VERDE_O   = (80, 180, 100)
DORADO    = (212, 175, 55)
GRIS      = (100, 100, 110)
GRIS_CL   = (160, 160, 175)
SOMBRA    = (10, 10, 18)

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
NOMBRES_P    = [p[0] for p in PERSONAJES]
PROFESION_P  = {p[0]: p[1] for p in PERSONAJES}

ARMAS      = ["Cuchillo", "Revolver", "Cuerda", "Llave inglesa", "Candelabro"]
LOCACIONES = ["Biblioteca", "Cocina", "Salon de baile", "Estudio", "Invernadero"]

# Descripcion ambiental de cada habitacion
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

# Objetos ambientales por habitacion (3 cada una). Una pista clave se anade dinamicamente.
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

# Actividades flavor que cada personaje puede mencionar en su coartada
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

# Texto del briefing inicial
BRIEFING_TEXTO = [
    "MADRUGADA DEL 14 DE OCTUBRE",
    "",
    "Lord Eustace Boddy, dueno de la Mansion Tudor en las afueras",
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

# 5 finales: uno por culpable
HISTORIAS = {
    "Coronel Mostaza": [
        "FINAL 1: EL HONOR PERDIDO",
        "",
        "El Coronel Mostaza, ahogado en deudas de juego,",
        "habia pedido un prestamo a Lord Boddy.",
        "Cuando este amenazo con revelar su deshonor",
        "ante el regimiento, el coronel actuo con la",
        "frialdad de un soldado en el campo de batalla.",
        "",
        "Su uniforme ya no oculta su crimen.",
    ],
    "Srta. Escarlata": [
        "FINAL 2: LA ESTRELLA APAGADA",
        "",
        "La Srta. Escarlata descubrio que Lord Boddy",
        "planeaba publicar un libro revelando su pasado",
        "y los escandalos que arruinarian su carrera.",
        "Bajo las luces del salon, decidio que el",
        "no veria el amanecer.",
        "",
        "Las luces de Hollywood se apagaron para Boddy.",
    ],
    "Prof. Ciruela": [
        "FINAL 3: EL EXPERIMENTO PROHIBIDO",
        "",
        "El Prof. Ciruela habia sido chantajeado",
        "durante anos por Lord Boddy, quien conocia",
        "sus experimentos ilegales con sustancias",
        "prohibidas por la academia.",
        "",
        "Esa noche, la ciencia y la venganza",
        "se mezclaron en una formula final.",
    ],
    "Sra. Blanco": [
        "FINAL 4: LOS ANOS DE SILENCIO",
        "",
        "La Sra. Blanco sirvio a Lord Boddy durante",
        "treinta anos, soportando humillaciones y",
        "desprecios. Cuando supo que seria despedida",
        "sin pension alguna, las llaves de la casa",
        "se convirtieron en su ultima arma.",
        "",
        "Treinta anos de silencio terminaron en un grito.",
    ],
    "Rev. Verde": [
        "FINAL 5: EL PASADO QUE NO PERDONA",
        "",
        "El Rev. Verde escondia un oscuro secreto",
        "bajo su sotana: una identidad robada anos atras",
        "tras un asesinato olvidado en el pueblo vecino.",
        "Lord Boddy lo habia descubierto y exigia",
        "confesion publica.",
        "",
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
    """Devuelve una lista de lineas que caben en ancho_max usando la fuente dada."""
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


# =============================================================
#                       LOGICA DEL JUEGO
# =============================================================
class Juego:
    def __init__(self):
        # MENU | BRIEFING | JUGANDO | HABITACION | INTERROGATORIO | ACUSANDO | FINAL
        self.estado = "MENU"
        self.iniciar_partida()
        self.crear_botones()

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

        # 4) Construir lista de objetos por habitacion (ambientales + 1 pista)
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

        # 5) Coartadas (interrogatorios)
        self.coartadas = {}
        for p in NOMBRES_P:
            if p == self.sol_personaje:
                # Culpable: miente -> dice una habitacion que NO sea la del crimen
                hab = random.choice([h for h in LOCACIONES if h != self.sol_locacion])
            else:
                # Inocente: cualquier habitacion (puede ser la del crimen o no)
                hab = random.choice(LOCACIONES)
            actividad = random.choice(ACTIVIDADES[p])
            self.coartadas[p] = (hab, actividad)

        # 6) Estado del jugador
        self.visitadas = set()
        self.descartados = {"personaje": set(), "arma": set(), "locacion": set()}
        self.objetos_examinados = set()  # set de (loc, idx)
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

        # JUGANDO: habitaciones
        self.btn_locaciones = []
        for i, loc in enumerate(LOCACIONES):
            self.btn_locaciones.append(
                Boton((60, 130 + i*80, 380, 70), loc, fuente=fuente_mediana))

        self.btn_interrogar = Boton((60, 580, 380, 60),
                                    "INTERROGAR SOSPECHOSOS",
                                    color=PANEL2, color_hover=DORADO,
                                    fuente=fuente_mediana)
        self.btn_acusar = Boton((60, 660, 380, 60),
                                "HACER ACUSACION FINAL",
                                color=(120, 30, 40), color_hover=ROJO,
                                fuente=fuente_mediana)

        # HABITACION
        self.btn_volver_hab = Boton((60, 720, 200, 50),
                                    "<- Volver al mapa", color=PANEL)
        # btn_objs se crean dinamicamente al entrar a una habitacion

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

    # ---------- Acciones ----------
    def entrar_habitacion(self, loc):
        self.locacion_actual = loc
        self.objeto_idx = None
        self.visitadas.add(loc)
        # Construir botones de objetos
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
    #                    DIBUJO POR PANTALLA
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

    def dibujar_briefing(self):
        dibujar_fondo()

        t = fuente_subtitulo.render("EXPEDIENTE DEL CASO", True, DORADO)
        ventana.blit(t, t.get_rect(center=(ANCHO//2, 50)))
        pygame.draw.line(ventana, DORADO,
                         (ANCHO//2 - 380, 90), (ANCHO//2 + 380, 90), 2)

        # Texto del briefing en la izquierda
        x_text = 80
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

        # Sospechosos en la derecha
        panel_x = 760
        panel_w = 460
        panel_rect = pygame.Rect(panel_x, 110, panel_w, 560)
        pygame.draw.rect(ventana, PANEL, panel_rect, border_radius=12)
        pygame.draw.rect(ventana, DORADO, panel_rect, 2, border_radius=12)
        ventana.blit(fuente_mediana.render("LOS 5 SOSPECHOSOS", True, DORADO),
                     (panel_x + 24, 125))

        for i, (nombre, prof, color) in enumerate(PERSONAJES):
            y = 175 + i*72
            pygame.draw.circle(ventana, color, (panel_x + 50, y + 22), 18)
            pygame.draw.circle(ventana, BLANCO, (panel_x + 50, y + 22), 18, 2)
            ventana.blit(fuente_texto.render(nombre, True, BLANCO),
                         (panel_x + 90, y + 4))
            ventana.blit(fuente_pequena.render(prof, True, GRIS_CL),
                         (panel_x + 90, y + 32))

        self.btn_briefing_continuar.dibujar(ventana)

    def dibujar_juego(self):
        dibujar_fondo()
        ventana.blit(fuente_subtitulo.render("Mansion Boddy", True, DORADO),
                     (60, 30))
        ventana.blit(fuente_pequena.render(
            f"Habitaciones investigadas: {len(self.visitadas)}/5  -  "
            f"Sospechosos interrogados: {len(self.interrogados)}/5",
            True, GRIS_CL), (60, 90))

        # Botones de habitaciones
        for i, btn in enumerate(self.btn_locaciones):
            btn.dibujar(ventana)
            if LOCACIONES[i] in self.visitadas:
                check = fuente_pequena.render("[VISITADA]", True, VERDE_O)
                ventana.blit(check,
                             (btn.rect.right - check.get_width() - 12,
                              btn.rect.bottom - 22))

        self.btn_interrogar.dibujar(ventana)
        self.btn_acusar.dibujar(ventana)

        # Cuaderno del Detective (panel derecho)
        panel_x, panel_w = 480, 740
        panel_rect = pygame.Rect(panel_x, 130, panel_w, 590)
        pygame.draw.rect(ventana, PANEL, panel_rect, border_radius=12)
        pygame.draw.rect(ventana, DORADO, panel_rect, 2, border_radius=12)
        ventana.blit(fuente_mediana.render("Cuaderno del Detective",
                                           True, DORADO),
                     (panel_x + 20, 145))

        col_w = (panel_w - 40) // 3
        cols = [
            ("SOSPECHOSOS", NOMBRES_P, "personaje"),
            ("ARMAS",       ARMAS,     "arma"),
            ("LOCACIONES",  LOCACIONES,"locacion"),
        ]
        for c, (tit, items, tipo) in enumerate(cols):
            cx = panel_x + 20 + c * col_w
            ventana.blit(fuente_texto.render(tit, True, BLANCO), (cx, 195))
            pygame.draw.line(ventana, DORADO,
                             (cx, 225), (cx + col_w - 10, 225), 1)
            for i, it in enumerate(items):
                desc = it in self.descartados[tipo]
                color = GRIS if desc else BLANCO
                if tipo == "personaje":
                    main = fuente_pequena.render(it, True, color)
                    prof = fuente_mini.render(PROFESION_P[it], True, GRIS)
                    ventana.blit(main, (cx, 245 + i*52))
                    ventana.blit(prof, (cx, 265 + i*52))
                    if desc:
                        y = 245 + i*52 + main.get_height()//2
                        pygame.draw.line(ventana, ROJO, (cx, y),
                                         (cx + main.get_width(), y), 2)
                else:
                    txt = fuente_pequena.render(it, True, color)
                    ventana.blit(txt, (cx, 245 + i*40))
                    if desc:
                        y = 245 + i*40 + txt.get_height()//2
                        pygame.draw.line(ventana, ROJO, (cx, y),
                                         (cx + txt.get_width(), y), 2)

        # Coartadas escuchadas (debajo del grid del cuaderno)
        if self.interrogados:
            ventana.blit(fuente_texto.render("Coartadas registradas:",
                                             True, DORADO),
                         (panel_x + 20, 540))
            for i, p in enumerate(sorted(self.interrogados,
                                         key=lambda x: NOMBRES_P.index(x))):
                hab, _ = self.coartadas[p]
                txt = f"- {p}: estaba en {hab}"
                surf = fuente_pequena.render(txt, True, GRIS_CL)
                ventana.blit(surf, (panel_x + 30, 575 + i*24))

    def dibujar_habitacion(self):
        dibujar_fondo()
        loc = self.locacion_actual

        # Encabezado
        t = fuente_subtitulo.render(loc, True, DORADO)
        ventana.blit(t, (60, 30))
        pygame.draw.line(ventana, DORADO, (60, 90), (1220, 90), 2)

        # Descripcion ambiental envuelta
        descr = DESCR_HABITACION[loc]
        lineas = envolver_texto(descr, fuente_texto, 1140)
        for i, l in enumerate(lineas):
            ventana.blit(fuente_texto.render(l, True, GRIS_CL),
                         (60, 110 + i*28))

        # Lista de objetos (izquierda)
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

        # Panel derecho: descripcion del objeto seleccionado
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

            # Texto descriptivo (puede tener \n)
            y_t = panel_rect.y + 80
            for parr in obj["desc"].split("\n"):
                lineas = envolver_texto(parr, fuente_texto,
                                         panel_rect.width - 40)
                for l in lineas:
                    ventana.blit(fuente_texto.render(l, True, BLANCO),
                                 (panel_rect.x + 20, y_t))
                    y_t += 30

            # Si era pista, marca
            if obj.get("es_pista"):
                aviso = fuente_pequena.render(
                    ">> Pista clave anadida al cuaderno <<", True, VERDE_O)
                ventana.blit(aviso,
                             (panel_rect.x + 20, panel_rect.bottom - 40))

        self.btn_volver_hab.dibujar(ventana)

    def dibujar_interrogatorio(self):
        dibujar_fondo()

        t = fuente_subtitulo.render("Sala de Interrogatorios", True, DORADO)
        ventana.blit(t, (60, 30))
        pygame.draw.line(ventana, DORADO, (60, 90), (1220, 90), 2)

        ventana.blit(fuente_pequena.render(
            "Selecciona a un sospechoso para preguntarle donde estuvo "
            "esa noche.", True, GRIS_CL), (60, 105))

        # Botones de sospechosos
        for i, btn in enumerate(self.btn_sospechosos):
            p = NOMBRES_P[i]
            btn.seleccionado = (p == self.personaje_int_actual)
            btn.dibujar(ventana)
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
            color_p = next(c for n, _, c in PERSONAJES if n == p)

            # Avatar circular
            cx, cy = panel_rect.x + 70, panel_rect.y + 70
            pygame.draw.circle(ventana, color_p, (cx, cy), 32)
            pygame.draw.circle(ventana, BLANCO, (cx, cy), 32, 2)

            ventana.blit(fuente_mediana.render(p, True, BLANCO),
                         (panel_rect.x + 120, panel_rect.y + 38))
            ventana.blit(fuente_pequena.render(PROFESION_P[p], True, GRIS_CL),
                         (panel_rect.x + 120, panel_rect.y + 70))

            pygame.draw.line(ventana, DORADO,
                             (panel_rect.x + 20, panel_rect.y + 130),
                             (panel_rect.right - 20, panel_rect.y + 130), 1)

            ventana.blit(fuente_mediana.render("Declaracion:", True, DORADO),
                         (panel_rect.x + 20, panel_rect.y + 150))

            decl = (f'"Estuve toda la noche en {hab}, {actividad}. '
                    f'No vi nada raro hasta que el mayordomo dio la alarma."')
            lineas = envolver_texto(decl, fuente_texto,
                                     panel_rect.width - 40)
            for i, l in enumerate(lineas):
                ventana.blit(fuente_texto.render(l, True, BLANCO),
                             (panel_rect.x + 20, panel_rect.y + 195 + i*30))

            nota = fuente_pequena.render(
                "Recuerda: el culpable mentira sobre su ubicacion.",
                True, GRIS_CL)
            ventana.blit(nota,
                         (panel_rect.x + 20, panel_rect.bottom - 35))

        self.btn_volver_int.dibujar(ventana)

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

    def dibujar_final(self):
        dibujar_fondo()
        if self.gano:
            t = fuente_subtitulo.render("CASO RESUELTO", True, VERDE_O)
            ventana.blit(t, t.get_rect(center=(ANCHO//2, 60)))
            sub_txt = (f"{self.sol_personaje}  -  {self.sol_arma}  -  "
                       f"{self.sol_locacion}")
            sub = fuente_mediana.render(sub_txt, True, DORADO)
            ventana.blit(sub, sub.get_rect(center=(ANCHO//2, 115)))
            pygame.draw.line(ventana, DORADO,
                             (ANCHO//2 - 420, 160),
                             (ANCHO//2 + 420, 160), 2)

            for i, linea in enumerate(HISTORIAS[self.sol_personaje]):
                f = fuente_mediana if i == 0 else fuente_texto
                color = DORADO if i == 0 else BLANCO
                surf = f.render(linea, True, color)
                ventana.blit(surf, surf.get_rect(
                    center=(ANCHO//2, 200 + i*42)))
        else:
            t = fuente_subtitulo.render("ACUSACION ERRONEA", True, ROJO)
            ventana.blit(t, t.get_rect(center=(ANCHO//2, 60)))

            tu = (f"Acusaste a {self.acu_personaje} "
                  f"con {self.acu_arma} en {self.acu_locacion}")
            ventana.blit(fuente_texto.render(tu, True, GRIS_CL),
                         fuente_texto.render(tu, True, GRIS_CL)
                         .get_rect(center=(ANCHO//2, 130)))

            ventana.blit(fuente_mediana.render(
                "Pero la verdad era...", True, BLANCO),
                fuente_mediana.render("Pero la verdad era...", True, BLANCO)
                .get_rect(center=(ANCHO//2, 195)))

            real = (f"{self.sol_personaje}  -  {self.sol_arma}  -  "
                    f"{self.sol_locacion}")
            ventana.blit(fuente_mediana.render(real, True, DORADO),
                         fuente_mediana.render(real, True, DORADO)
                         .get_rect(center=(ANCHO//2, 245)))

            pygame.draw.line(ventana, DORADO,
                             (ANCHO//2 - 420, 290),
                             (ANCHO//2 + 420, 290), 2)

            for i, linea in enumerate(HISTORIAS[self.sol_personaje][2:]):
                surf = fuente_texto.render(linea, True, BLANCO)
                ventana.blit(surf, surf.get_rect(
                    center=(ANCHO//2, 330 + i*32)))

            cierre = fuente_texto.render(
                "El verdadero culpable escapo. Caso cerrado.", True, ROJO)
            ventana.blit(cierre, cierre.get_rect(
                center=(ANCHO//2, 660)))

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
            for btn in self.btn_locaciones:
                btn.actualizar(mouse)
            self.btn_interrogar.actualizar(mouse)
            self.btn_acusar.actualizar(mouse)
            for ev in eventos:
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