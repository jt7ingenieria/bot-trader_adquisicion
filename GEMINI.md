# Project: Adquisición de Datos y Backtesting

Este documento sirve como una guía rápida para entender y retomar el desarrollo del proyecto `adquisicion_de_datos_modulo_listo`.

## 1. Entorno Virtual

Para trabajar en este proyecto, es **esencial** activar el entorno virtual dedicado.

**Ruta del Entorno Virtual:**
`C:\Users\javie\modulos bot\entorno_virtual_modulo`

**Cómo activar el entorno virtual:**
```bash
C:\Users\javie\modulos bot\entorno_virtual_modulo\Scripts\activate.bat
```

## 2. Dependencias

Las dependencias del proyecto se instalaron manualmente ya que no se encontró un archivo `requirements.txt`.

**Comando para instalar dependencias (dentro del entorno virtual activado):**
```bash
pip install fastapi uvicorn pandas
```
**Nota:** Es posible que se necesiten otras librerías como `loguru`, `pandas_ta`, `python-dotenv`, `ccxt`, `scikit-learn`. Si encuentras errores de `ModuleNotFoundError`, instálalas con `pip install <nombre_libreria>`.

## 3. Correcciones Realizadas

Durante la última sesión, se realizaron las siguientes correcciones para resolver errores de `ModuleNotFoundError` y `OSError`:

*   **Corrección de importaciones relativas:**
    *   En `src/modes/historical.py`: Se cambió `from src.config import Config` a `from config import Config` y `from src.data_fetcher import AsyncCryptoDataFetcher` a `from data_fetcher import AsyncCryptoDataFetcher`.
    *   En `src/modes/indicators.py`: Se cambió `from src.config import Config` a `from config import Config`.
    *   En `src/modes/realtime.py`: Se cambió `from src.config import Config` a `from config import Config` y `from src.data_fetcher import AsyncCryptoDataFetcher` a `from data_fetcher import AsyncCryptoDataFetcher`.
    *   En `src/strategy.py`: Se cambió `from src.config import Config` a `from config import Config`.
*   **Creación del directorio de salida:**
    *   Se creó el directorio `data/` en la raíz del proyecto, ya que el script intentaba guardar archivos en él y no existía.

## 4. Cómo Ejecutar el Proyecto (`main.py`)

El script principal `main.py` soporta varios modos de operación.

**Sintaxis general:**
```bash
python main.py --mode <modo> [opciones_adicionales]
```

**Modos disponibles:**

*   **`historical`**: Descarga y procesa datos históricos de criptomonedas.
    *   **Comando:** `python main.py --mode historical`
    *   **Estado actual:** Funcional. Descarga datos y calcula indicadores, guardándolos en el directorio `data/`.
*   **`indicators`**: Calcula indicadores técnicos sobre datos existentes.
    *   **Comando:** `python main.py --mode indicators`
    *   **Estado actual:** Las importaciones han sido corregidas, pero no se ha probado su ejecución completa.
*   **`realtime`**: Fetches data in real-time.
    *   **Comando:** `python main.py --mode realtime`
    *   **Estado actual:** Las importaciones han sido corregidas, pero no se ha probado su ejecución completa.
*   **`preprocessing`**: Preprocesa un archivo CSV dado.
    *   **Comando:** `python main.py --mode preprocessing --filepath <ruta_al_archivo.csv>`
    *   **Estado actual:** No se ha probado su ejecución.
*   **`backtest`**: Ejecuta un backtest con una estrategia específica sobre un archivo CSV preprocesado.
    *   **Comando:** `python main.py --mode backtest --filepath <ruta_al_archivo_procesado.csv> --strategy <nombre_estrategia>`
    *   **Estrategias disponibles:** `moving_average_crossover_strategy`, `ema_volume_strategy`
    *   **Estado actual:** No se ha probado su ejecución.

## 5. Próximos Pasos y Tareas Pendientes

Para continuar el desarrollo, se recomienda:

1.  **Probar y verificar los modos restantes:**
    *   Ejecutar `python main.py --mode indicators` y verificar la salida.
    *   Ejecutar `python main.py --mode realtime` (considerar que este modo es un bucle infinito y puede requerir interrupción manual).
    *   Generar un archivo de datos (usando `historical` o manualmente), luego ejecutar `python main.py --mode preprocessing --filepath <ruta_al_archivo.csv>` y verificar el archivo procesado.
    *   Con un archivo procesado, ejecutar `python main.py --mode backtest --filepath <ruta_al_archivo_procesado.csv> --strategy moving_average_crossover_strategy` y `python main.py --mode backtest --filepath <ruta_al_archivo_procesado.csv> --strategy ema_volume_strategy` para probar las estrategias de backtesting.
2.  **Desarrollo de la API FastAPI:**
    *   Los endpoints `/api/performance` y `/api/signals` en `main.py` están definidos pero su lógica interna aún no está implementada (`"message": "Performance data will be here"`).
    *   Considerar cómo se integrará el dashboard (`dashboard/app.py`) con estos endpoints.
3.  **Revisión y mejora de la configuración:**
    *   Asegurarse de que todas las variables en `config.py` sean adecuadas y estén bien documentadas.
    *   Considerar la creación de un archivo `.env.example` para facilitar la configuración a otros desarrolladores.
4.  **Implementación de pruebas unitarias:**
    *   Desarrollar pruebas para las funciones clave en `data_fetcher.py`, `preprocessing.py`, `strategy.py`, `backtesting_engine.py`, y `performance_analyzer.py` para asegurar la robustez del código.
5.  **Documentación adicional:**
    *   Añadir comentarios al código donde sea necesario para explicar lógica compleja.
    *   Considerar la creación de un `README.md` más detallado para el proyecto.
