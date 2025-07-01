<p align="center">
  <img width="150px" src="https://i.ibb.co/bXvzjXm/LOGO-h1.png" alt="H1 Logo">
  <img width="150px" src="https://github.com/user-attachments/assets/e0551b39-11a1-4ce3-b5e2-2c6c18882bf0" alt="Project Logo">
</p>

# Skolagh UI Team

# SkolaghButton Documentation

This README provides a complete reference for the `SkolaghButton-*` component classes used in the Skolagh theme. Each button is styled with Tailwind CSS using `@apply`, and provides consistent styling across various color variants.

## 🧩 Usage

Apply a color-specific button by using:

```html
<a href="#" class="SkolaghButton-COLOR">Click me</a>
```

Replace `COLOR` with one of the supported color variants.

## 🎨 Available Colors

| Class Name             | Description               |
| ---------------------- | ------------------------- |
| `SkolaghButton-red`    | Deep red background       |
| `SkolaghButton-blue`   | Royal blue background     |
| `SkolaghButton-green`  | Classic green background  |
| `SkolaghButton-yellow` | Bright yellow, black text |
| `SkolaghButton-purple` | Deep purple               |
| `SkolaghButton-pink`   | Soft pink background      |
| `SkolaghButton-gray`   | Neutral gray background   |
| `SkolaghButton-cyan`   | Cool cyan                 |
| `SkolaghButton-teal`   | Teal (green-blue)         |
| `SkolaghButton-lime`   | Lime green, black text    |
| `SkolaghButton-indigo` | Dark indigo               |
| `SkolaghButton-rose`   | Rose pink                 |
| `SkolaghButton-orange` | Default orange style      |

## 🧪 Example

```html
<a href="#" class="SkolaghButton-green">Confirm</a>
<a href="#" class="SkolaghButton-yellow">Warning</a>
<a href="#" class="SkolaghButton-pink">Romantic</a>
```

## ⚙️ Internals

Each button class applies the following Tailwind styles:

* `font-semibold`
* `text-white` or `text-black` (depends on color)
* `px-2 py-2`
* `rounded-lg`
* `text-center text-lg`
* `bg-{color}-600` or similar
* `border-l border-r border-t border-4 border-{color}-800`
* `focus:border focus:mt-1`

## ✅ Best Practices

* Use `text-black` only on light backgrounds (e.g., yellow or lime).
* Keep consistency by using these utility classes instead of redefining styles inline.
* Combine with icons or additional utilities for complex components.

## 📁 File Location

You can find or modify these classes inside your Tailwind CSS input file, likely in:

```
theme/static/css/src/input.css
```

Make sure to recompile Tailwind with:

```bash
npx tailwindcss -i ./theme/static/css/src/input.css -o ./theme/static/css/dist/styles.css --minify
```

---

Made with 🧡 by the Skolagh UI Team.
