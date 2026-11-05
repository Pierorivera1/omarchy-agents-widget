# Instrucciones para agentes

- Lee README.md antes de instalar o modificar el widget. Su objetivo es replicar la copia del laptop en otro equipo con Omarchy.
- Inspecciona la instalación y las instrucciones locales. No edites `/usr/share/omarchy/`.
- Mantén la sincronización, sus tiempos y los ajustes existentes del equipo. No copies un shell.json completo ni configuración personal del laptop.
- Conserva el ID `pierooo.agents` y los identificadores internos de módulo/IPC `omarchy.agents`. El prefijo del plugin no depende del usuario local.
- Respalda fuera de la carpeta de plugins. No descartes personalizaciones sin autorización.
- No incluyas credenciales, estadísticas, conversaciones, cachés, snapshots o capturas personales en commits.
- No cambies el stack ni instales dependencias sin explicar la necesidad.
- Ejecuta las pruebas de Python, la comprobación de Bash y la validación del manifiesto. Después de instalar, verifica el panel visualmente.
- Reiniciar Omarchy Shell puede ser necesario para cargar Main.qml actualizado. No lo reinicies con la sesión bloqueada.
- Reporta qué cambió, qué verificaste y cualquier incompatibilidad. No afirmes ahorros de batería sin mediciones.
