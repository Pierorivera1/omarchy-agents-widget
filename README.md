# Omarchy agents widget

Widget personal de Omarchy para ver límites de suscripción y estadísticas de Codex, Claude Code y Antigravity. Este repositorio contiene la copia completa instalada en el laptop de Piero, con sus cambios locales. Está preparado para que otro agente lo replique en un desktop con Omarchy.

## Instrucción para el agente del desktop

> Lee README.md y AGENTS.md. Inspecciona mi instalación de Omarchy y replica este widget. Conserva mi configuración, mi sincronización y sus tiempos. Instala los archivos del repositorio, verifica los recolectores y confirma visualmente el orden Codex, Claude Code, Antigravity. No copies credenciales ni estadísticas de otra máquina. Si falta una dependencia o la versión de Omarchy es incompatible, explica el problema antes de cambiar el sistema.

## Qué incluye

- Pestañas en orden Codex, Claude Code y Antigravity. Los demás proveedores descubiertos aparecen después, ordenados por identificador.
- Selección por identificador, para que una actualización no cambie la pestaña elegida. Al cargar el widget comienza por el primer proveedor disponible; al cerrar y abrir recuerda la selección mientras sigue cargado.
- Actualizaciones locales limitadas por defecto a `codex`, `claude` y `agy`, en lugar de lanzar todos los recolectores de Omarchy.
- Recolector local de Codex que omite eventos repetidos cuando el total acumulado de tokens no cambia. Mantiene turnos distintos con el mismo consumo si el acumulado avanza.
- Ruta del actualizador relativa al plugin, sin depender del nombre de usuario.
- Animaciones que respetan `Style.duration()`.
- Sincronización entre equipos heredada del widget original. Su implementación y sus temporizadores no se modificaron.
- Cinco pruebas de regresión para el conteo de Codex.

No incluye archivos de configuración completos del laptop, credenciales, conversaciones, estadísticas, cachés ni capturas de pantalla.

## Requisitos y compatibilidad

La instalación de origen utiliza Omarchy `4.5.0-3`, Quickshell y Qt Quick. Esto es una referencia probada, no una promesa de compatibilidad con cualquier versión.

Antes de instalar, el agente debe comprobar:

- Que existen `omarchy`, `omarchy-shell`, `python`, `bash`, `jq`, `find` y `readlink`. El recolector busca también `rg` para sesiones de pi/omp y el ejecutable `codex` para consultar límites.
- Que están disponibles los módulos QML `qs.Commons`, `qs.Ui` y `Quickshell.Io`, y que `qs.Commons.Style` ofrece `duration()`.
- Que `$OMARCHY_PATH/bin` contiene `omarchy-agent-usage-claude` y `omarchy-agent-usage-agy`. Se usan los recolectores de la instalación de destino, no copias de este repositorio.
- Que Codex puede ejecutar `app-server` y responder a `initialize`, `account/read` y `account/rateLimits/read`. El recolector tiene tiempos de espera y muestra el error si no puede consultar límites.
- Que las herramientas que se desean usar estén autenticadas en el desktop. El widget no inicia sesión por el usuario.

No instales dependencias ni actualices Omarchy sin explicar antes por qué hacen falta.

## Instalación desde el clon

```bash
gh repo clone Pierorivera1/omarchy-agents-widget
cd omarchy-agents-widget
python -m unittest discover -s tests -v
bash -n scripts/omarchy-agent-usage-update
omarchy plugin validate "$PWD"
```

El repositorio es privado; el desktop necesita acceso autenticado a GitHub.

### 1. Inspeccionar y respaldar

Lee `~/.config/omarchy/shell.json` y los plugins existentes. El identificador de este widget es `pierooo.agents`, independientemente del nombre de usuario del desktop. Mantén los identificadores internos `omarchy.agents` de QML: corresponden al módulo y a su IPC, no al directorio de instalación.

Antes de cambiar archivos, guarda una copia fechada de `shell.json` y del directorio `~/.config/omarchy/plugins/pierooo.agents`, si existe. Guarda los respaldos fuera del directorio de plugins para que Omarchy no intente descubrirlos.

Si ya existe una versión personalizada, revisa las diferencias antes de reemplazarla. No descartes personalizaciones ni datos sin autorización.

### 2. Copiar el plugin

Para una instalación nueva, desde la raíz del repositorio:

```bash
python - <<'PY'
from pathlib import Path
import shutil
source = Path.cwd()
destination = Path.home() / '.config/omarchy/plugins/pierooo.agents'
if destination.exists() or destination.is_symlink():
    raise SystemExit('El destino ya existe. Revisar y respaldar antes de actualizar.')
destination.mkdir(parents=True)
for name in ('Main.qml', 'Panel.qml', 'Agent.qml', 'manifest.json'):
    shutil.copy2(source / name, destination / name)
for name in ('assets', 'scripts'):
    shutil.copytree(source / name, destination / name,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
PY
```

Se conservan los permisos ejecutables de ambos scripts. Este procedimiento no copia `.git`, pruebas ni documentación a la carpeta vigilada por Omarchy.

### 3. Integrar sin reemplazar la configuración

```bash
omarchy-shell shell rescanPlugins
omarchy plugin enable pierooo.agents --section right
```

El manifiesto declara `clonedFrom: omarchy.agents`. Verifica que el clon reemplace al widget original y que no queden dos iconos. Si hace falta ajustar la ubicación, conserva la posición anterior del widget y el orden de los demás elementos de la barra.

No reemplaces `shell.json` por un archivo del repositorio. Si el desktop ya tiene ajustes del widget original, conserva sus valores en la entrada del clon, incluidos `providers`, `refreshIntervalSec`, `syncMode`, `syncDir`, `syncFileName` y `syncDeviceId`. No cambies la carpeta compartida ni los tiempos. Si ambos equipos comparten carpeta, verifica que tengan nombres de snapshot e identificadores de dispositivo distintos; informa cualquier colisión antes de cambiar esos valores.

Una instalación nueva usa los valores predeterminados del manifiesto: actualización cada 900 segundos y sincronización desactivada. El repositorio no contiene los ajustes personales de sincronización del laptop. Si el desktop no tiene ajustes previos y Piero quiere sincronizar los equipos, pide la carpeta y los identificadores que desea usar. No inventes esa configuración.

### 4. Recargar y verificar

La recarga automática no actualizó de forma fiable el componente `Main.qml` en la instalación de origen. Después de instalar o actualizar:

```bash
omarchy restart shell
omarchy-shell omarchy.agents refresh
omarchy-shell omarchy.agents open
```

La recarga reinicia la selección inicial. No reinicia el desktop. No reinicies el shell si la sesión está bloqueada.

Verifica visualmente el panel. Que un comando termine sin error no demuestra que el componente activo haya cargado los cambios.

## Datos y arquitectura

| Archivo | Responsabilidad |
| --- | --- |
| `Panel.qml` | Icono de barra, panel, pestañas, límites, gráficos, teclado e IPC. |
| `Main.qml` | Descubrimiento de registros, actualización, orden de proveedores y sincronización. |
| `Agent.qml` | Lectura y vigilancia del JSON de un proveedor. |
| `scripts/omarchy-agent-usage-update` | Ejecuta recolectores y escribe registros mediante reemplazo atómico. |
| `scripts/omarchy-agent-usage-codex` | Estadísticas locales y límites de Codex mediante app-server. |
| `manifest.json` | Identidad, valores predeterminados y esquema de ajustes. |
| `tests/test_codex_usage.py` | Regresión del conteo de eventos de Codex. |

Los registros se guardan en `${XDG_STATE_HOME:-$HOME/.local/state}/omarchy/agents/usage/`. El JSON incluye identidad, límites, estadísticas por día/modelo y metadatos. El panel descubre registros locales y puede agregar snapshots de otros equipos con la lógica original.

Codex lee `sessions` y `archived_sessions` dentro de `${CODEX_HOME:-$HOME/.codex}`, además de sesiones compatibles de pi/omp y opencode. Los archivos nativos se seleccionan por fecha de modificación dentro de los últimos 30 días; se procesa su contenido completo. Por tanto, los totales por modelo no representan necesariamente 30 días exactos ni todo el historial.

La caché local de Codex reside en `${XDG_CACHE_HOME:-$HOME/.cache}/omarchy/agent-usage/`. Un refresco normal puede reutilizarla durante 20 segundos, y `--limits-only` durante 900 segundos. `--force` vuelve a escanear. Estos tiempos se conservaron.

El actualizador local acepta `--force`, `--limits-only`, `--except <id>` y proveedores explícitos. Por ejemplo, desde el repositorio:

```bash
scripts/omarchy-agent-usage-update --force codex
scripts/omarchy-agent-usage-update --limits-only --except claude
```

Otros proveedores pueden seguir apareciendo si otro proceso escribe sus registros. Para añadir uno a las actualizaciones automáticas, modifica la lista predeterminada del actualizador de forma explícita.

## Sincronización

El widget conserva los ajustes y el código de sincronización originales. `syncMode` y `syncDir` controlan la función. Con sincronización configurada, el widget escribe el snapshot de este dispositivo y combina los snapshots JSON de la carpeta. El programa que transporta la carpeta entre equipos, como Syncthing, se configura por separado.

Los cambios en registros programan la sincronización con el debounce original de 1000 ms. El refresco periódico conserva `refreshIntervalSec`; el panel abierto mantiene su temporizador de 30 segundos para actualizar textos de cuenta regresiva. No confundas esos temporizadores con el transporte entre equipos.

No publiques snapshots, rutas personales de sincronización ni estadísticas en este repositorio. No borres la carpeta de sincronización para reinstalar o desinstalar el widget.

## Validación y límites conocidos

```bash
python -m unittest discover -s tests -v
bash -n scripts/omarchy-agent-usage-update
omarchy plugin validate "$PWD"
```

Las pruebas cubren duplicados, turnos diferentes con igual consumo, eventos sin acumulado, independencia entre sesiones y reinicio del acumulado. No requieren credenciales ni consultan la red.

Comprueba además en el desktop:

1. Codex a la izquierda, Claude Code en medio y Antigravity a la derecha, cuando los tres tengan datos.
2. Que cerrar y abrir recuerde la selección, y que refrescar no la cambie.
3. Que el panel siga funcionando cuando un proveedor no esté autenticado o no tenga datos. No fuerces pestañas con estadísticas inventadas.
4. Que solo se actualicen los tres recolectores predeterminados y que el registro de Codex tenga una fecha nueva.
5. Que los valores de sincronización y los tiempos existentes sigan iguales después de instalar.

El clon conserva recursos limitados: no incluye un SVG específico de Antigravity, por lo que utiliza el icono genérico y puede registrar una advertencia por el SVG ausente. Eso no impide mostrar datos. La lista por modelo muestra los cuatro primeros, como en el widget instalado.

El widget comparte proceso con Omarchy Shell. La RAM de `quickshell` incluye otros componentes y no mide por sí sola este widget. Limitar recolectores reduce trabajo periódico; no hay una medición que cuantifique el ahorro de batería.

## Actualizar o volver atrás

Este procedimiento instala una copia, no una carpeta Git. Para actualizar, revisa el diff del nuevo commit, respalda los archivos instalados y copia únicamente los archivos del plugin. Conserva la configuración del desktop. Después valida y reinicia el shell.

Para revertir, restaura los archivos respaldados y la configuración solo si hace falta, preservando cualquier cambio posterior del usuario. No borres estadísticas, credenciales, cachés ni snapshots. Reinicia el shell y comprueba el panel.

## Origen y licencia

Derivado del widget `omarchy.agents` de [Omarchy](https://github.com/basecamp/omarchy), con modificaciones locales de Piero. El manifiesto conserva la atribución original. Se incluye la licencia MIT de Omarchy en `LICENSE`. Este proyecto no es un plugin oficial de Omarchy.
