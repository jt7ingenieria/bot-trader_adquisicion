# Bot Trader: Adquisición de Datos (v1.0)

Este proyecto es un bot trader enfocado en la adquisición y procesamiento de datos de criptomonedas, backtesting de estrategias y visualización de resultados. Está diseñado para ser modular y extensible.

## Estructura del Proyecto

```
. (src)
├───__init__.py
├───backtesting_engine.py
├───config.py
├───data_fetcher.py
├───main.py
├───performance_analyzer.py
├───preprocessing.py
├───strategy.py
├───__pycache__/
├───dashboard/
│   ├───app.py
│   ├───__pycache__/
│   ├───static/
│   └───templates/
│       └───index.html
├───frontend/
│   ├───components.json
│   ├───eslint.config.js
│   ├───index.html
│   ├───package.json
│   ├───postcss.config.js
│   ├───tailwind.config.ts
│   ├───tsconfig.app.json
│   ├───tsconfig.json
│   ├───tsconfig.node.json
│   └───vite.config.ts
├───modes/
│   ├───historical.py
│   ├───indicators.py
│   ├───realtime.py
│   └───__pycache__/
├───utils/
│   ├───__init__.py
│   ├───logger_config.py
│   └───__pycache__/
├───.gitignore
├───GEMINI.md
└───requirements.txt
```

## Requisitos

*   Python 3.9+

## Configuración del Entorno

1.  **Activar el Entorno Virtual:**
    Es crucial activar el entorno virtual antes de instalar dependencias o ejecutar el proyecto.
    ```bash
    C:\Users\javie\modulos bot\entorno_virtual_modulo\Scripts\activate.bat
    ```

2.  **Instalar Dependencias:**
    Una vez activado el entorno virtual, instala las dependencias listadas en `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    Si `requirements.txt` no existe o está incompleto, las dependencias principales son:
    ```bash
    pip install fastapi uvicorn pandas loguru pandas_ta python-dotenv ccxt scikit-learn
    ```

## Uso

El script principal `main.py` permite ejecutar diferentes modos de operación.

**Sintaxis general:**

```bash
python main.py --mode <modo> [opciones_adicionales]
```

### Modos Disponibles:

*   **`historical`**: Descarga y procesa datos históricos de criptomonedas.
    ```bash
    python main.py --mode historical
    ```

*   **`indicators`**: Calcula indicadores técnicos sobre datos existentes.
    ```bash
    python main.py --mode indicators
    ```

*   **`realtime`**: Fetches data in real-time.
    ```bash
    python main.py --mode realtime
    ```

*   **`preprocessing`**: Preprocesa un archivo CSV dado.
    ```bash
    python main.py --mode preprocessing --filepath <ruta_al_archivo.csv>
    ```

*   **`backtest`**: Ejecuta un backtest con una estrategia específica sobre un archivo CSV preprocesado.
    *   **Estrategias disponibles:** `moving_average_crossover_strategy`, `ema_volume_strategy`
    ```bash
    python main.py --mode backtest --filepath <ruta_al_archivo_procesado.csv> --strategy moving_average_crossover_strategy
    ```

## Notas Importantes

*   **Correcciones de Importación:** Se han corregido rutas de importación relativas en varios módulos (`modes/historical.py`, `modes/indicators.py`, `modes/realtime.py`, `strategy.py`) para resolver errores de `ModuleNotFoundError`.
*   **Directorio de Datos:** El proyecto espera un directorio `data/` en la raíz para guardar los archivos de salida. Si no existe, se creará automáticamente al ejecutar el modo `historical`.
*   **`GEMINI.md`:** Para un registro detallado de las correcciones, el entorno virtual y los pasos de desarrollo, consulte el archivo `GEMINI.md`.

## Próximos Pasos

1.  Completar la implementación de los modos `indicators`, `realtime`, `preprocessing` y `backtest`.
2.  Desarrollar la lógica para los endpoints de la API FastAPI en `main.py` (`/api/performance`, `/api/signals`).
3.  Integrar el dashboard con la API.
4.  Implementar pruebas unitarias para las funciones clave.
5.  Revisar y mejorar la configuración en `config.py`.
