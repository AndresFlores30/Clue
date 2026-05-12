# Clue
```markdown
# CLUE - Simulador de Misterio

Un juego de deducción donde tendrás que investigar un asesinato en la mansión, examinar objetos, interrogar sospechosos y descubrir al culpable, el arma y la habitación donde ocurrió el crimen.

---

## Instalación

Instrucciones para instalar y ejecutar el simulador Clue.

### Paso 1. Instalar Python

Si todavía no lo tienes instalado, descárgalo desde la página oficial [python.org/downloads](https://python.org/downloads). Cuando lo instales en Windows, es muy importante marcar la casilla **"Add Python to PATH"** antes de presionar el botón Install. En Mac y Linux normalmente ya viene instalado.

### Paso 2. Instalar la librería Pygame

Abre la terminal del sistema:
- **Windows**: Presiona `Windows + R`, escribe `cmd` y presiona Enter.
- **Mac**: Abre la aplicación Terminal.
- **Linux**: Usa tu terminal preferida.

Una vez abierta, escribe el siguiente comando y presiona Enter:

```bash
pip install pygame
```

Espera unos segundos hasta que termine la descarga e instalación.

### Paso 3. Organizar los archivos del juego

Crea una carpeta en cualquier lugar de tu computadora (por ejemplo, en el Escritorio) y nómbrala `Clue`. Dentro de esa carpeta coloca el archivo `clue.py`. 

Después crea una subcarpeta llamada `imagenes` (sin acento, todo en minúsculas) y dentro de ella coloca las seis imágenes del juego:

- `Tablero.png`
- `Coronel_Mostaza.png`
- `Señorita_Escarlata.png`
- `Profesor_Ciruela.png`
- `Señora_Blanco.png`
- `Reverendo_Verde.png`

**Importante:** Los nombres deben coincidir exactamente como están escritos aquí.

### Paso 4. Ejecutar el juego

Tienes dos formas de hacerlo:

1. **Método simple:** Haz doble clic sobre el archivo `clue.py`.
2. **Método por terminal:** Abre la terminal, navega hasta la carpeta del juego y escribe:

```bash
python clue.py
```

---

## Solución de problemas comunes

| Problema | Solución |
|----------|----------|
| `'python' no se reconoce como comando` | No marcaste la opción "Add Python to PATH" durante la instalación. Reinstala Python marcando esa casilla. |
| `ModuleNotFoundError` relacionado con pygame | Faltó instalar la librería. Vuelve al Paso 2. |
| El juego abre pero los personajes aparecen como círculos de colores en lugar de retratos | La carpeta `imagenes` está mal nombrada, en otra ubicación o falta algún archivo. Revisa los nombres y la ubicación según el Paso 3. |

---

## Cómo jugar

1. **Lee el briefing inicial** para conocer los detalles del caso.
2. **Explora las habitaciones** de la mansión haciendo clic en el tablero.
3. **Examina los objetos** de cada sala para encontrar pistas.
4. **Interroga a los sospechosos** para conocer sus coartadas.
5. **Usa el cuaderno del detective** para llevar registro de las pistas y descartes.
6. **Realiza tu acusación final** cuando creas tener la respuesta correcta.

---

## Estructura de archivos esperada

```
Clue/
├── clue.py
└── imagenes/
    ├── Tablero.png
    ├── Coronel_Mostaza.png
    ├── Señorita_Escarlata.png
    ├── Profesor_Ciruela.png
    ├── Señora_Blanco.png
    └── Reverendo_Verde.png
```

**Nota:** Si la carpeta `imagenes` o alguno de los archivos de imagen no existe, el juego seguirá funcionando con una representación alternativa en formas y colores.

---

## Requisitos

- Python 3.6 o superior
- Pygame (`pip install pygame`)

---

## Créditos

Caso clásico de misterio - 5 finales posibles

---

¡Buena suerte, detective!
```