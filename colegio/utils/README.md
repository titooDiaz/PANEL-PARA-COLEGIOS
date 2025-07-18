<p align="center">
  <img width="150px" src="https://i.ibb.co/bXvzjXm/LOGO-h1.png" alt="Logo de h1">
  <img width="150px" src="https://github.com/user-attachments/assets/e0551b39-11a1-4ce3-b5e2-2c6c18882bf0" alt="Logo del proyecto">
</p>

# 📁 `utils` Folder

## Description

The `utils` folder contains reusable functions, classes, and code snippets that support the **backend** logic of the school panel.
Its main goal is to **avoid code repetition** (_DRY: Don't Repeat Yourself_), **improve maintainability**, and **facilitate scalability** of the project.

---

## Why use `utils`?

- ✅ **Avoid code duplication:** Common functions are centralized in one place.
- ✅ **Facilitate maintenance:** If you need to update shared logic, you only have to do it once.
- ✅ **Improve organization:** Separate "what is done" from "how it is done," making your backend cleaner and more modular.
- ✅ **Ease testing:** Utilities are small and isolated, making them easier to test individually.
- ✅ **Promote best practices:** Clearer and more professional code, following software engineering principles.

---

## What to include in `utils`?

In this folder, you can include:

- Data validation functions
- Date and time formatting utilities
- File handling utilities
- Mathematical or conversion functions
- Authentication or authorization helpers
- Any piece of common logic that you use across multiple modules

---

## Suggested structure

```plaintext
utils/
├── auth_utils.py         # Authentication-related functions
├── date_utils.py         # Date formatting and manipulation
├── file_utils.py         # File handling utilities
├── math_utils.py         # Mathematical calculations or conversions
├── validations.py        # Common validations
└── __init__.py           # Enables easy imports of utilities
```

> You can organize additional subfolders if the project grows.

---

# 🕒 Timezone Utils

Minimal and lively documentation for timezone-based user utilities in Python.

---

## `get_user_timezone(user)`  
🔹 **Returns:** User's timezone string.

**Args:**  
- `user`: Has a `time_zone` attribute.

**Usage:**  
```python
tz = get_user_timezone(user)
```

---

## `get_current_date(user)`  
📅 **Returns:** Current date (YYYY-MM-DD) in user's timezone.

**Args:**  
- `user`: User object.

**Usage:**  
```python
date = get_current_date(user)
```

---

## `get_current_time(user)`  
⏰ **Returns:** Current time (no seconds/microseconds) in user's timezone.

**Args:**  
- `user`: User object.

**Usage:**  
```python
time = get_current_time(user)
```

---

## `get_midnight(user)`  
🌙 **Returns:** `datetime` at 23:59 in user's timezone.

**Args:**  
- `user`: User object.

**Usage:**  
```python
midnight = get_midnight(user)
```

---
✨ Simple, clear, and timezone aware!

## Final notes

- Keep utility functions **as generic as possible**.
- Add comments and docstrings to explain the purpose of each utility.
- If a function grows too much or becomes module-specific, consider moving it elsewhere.

---

# 🚀 With a strong `utils` folder, your project will be cleaner, more maintainable, and highly scalable!

