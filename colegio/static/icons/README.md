<p align="center">
  <img width="150px" src="https://i.ibb.co/bXvzjXm/LOGO-h1.png" alt="Logo de h1">
  <img width="150px" src="https://github.com/user-attachments/assets/e0551b39-11a1-4ce3-b5e2-2c6c18882bf0" alt="Logo del proyecto">
</p>

# Uso de Iconos en el Proyecto

## Introducción
Este documento explica cómo agregar iconos de manera ortogonal en el proyecto, permitiendo reutilización y facilidad de mantenimiento.

## Estructura General
Para incluir un icono en cualquier parte de la interfaz, usa la siguiente estructura:

```html
<div class="w-6 h-6 bg-white flex mask-icon" data-icon="{% static 'icons/ICONO' %}"></div>
<script src="{% static 'icons/icons.js' %}"></script>
<link href="{% static 'icons/icons.css' %}" rel='stylesheet'/>
```

Donde `ICONO` debe ser reemplazado por el nombre del archivo SVG correspondiente.

## Explicación de los Elementos
- `<div class="w-6 h-6 bg-white flex mask-icon" data-icon="{% static 'icons/ICONO' %}"></div>`
  - `w-6 h-6` define el tamaño del icono.
  - `bg-white` establece el color del icono (se puede modificar con Tailwind CSS).
  - `mask-icon` es la clase encargada de aplicar la máscara SVG.
  - `data-icon` almacena la URL del icono SVG.

- `<script src="{% static 'icons/icons.js' %}"></script>`
  - Este script se encarga de leer el atributo `data-icon` y aplicar la máscara correspondiente.

- `<link href="{% static 'icons/icons.css' %}" rel='stylesheet'/>`
  - (Opcional) Si los estilos de los iconos estuvieran en un archivo CSS, podría usarse un `link` para importarlos.

## Uso en Botones
Para incluir un icono dentro de un botón sin que haya saltos de línea, usa la siguiente estructura:

```html
<button class="inline-flex items-center space-x-2 text-white bg-orange-600 px-2 py-2 rounded-lg border-4 border-orange-800 hover:scale-105 transition duration-300 ease-in-out">
    <div class="w-6 h-6 bg-white mask-icon" data-icon="{% static 'icons/information/pencil.svg' %}"></div>
    <span>Editar actividad</span>
</button>
```

## Consideraciones
- Asegúrate de que `icons.js` se cargue correctamente en la página.
- Puedes cambiar el color del icono con clases de Tailwind como `bg-red-500`, `bg-blue-400`, etc.
- Todos los iconos deben estar en la carpeta `static/icons/`.

## Conclusión
Este método permite incluir iconos SVG de manera flexible y reutilizable en el proyecto, asegurando que los cambios sean fáciles de aplicar sin modificar cada componente individualmente.