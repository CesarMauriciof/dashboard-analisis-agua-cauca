# Despliegue en GitHub y Streamlit Community Cloud

**Proyecto:** IRCA Cauca 2007–2025  
**Grupo:** 4  
**Fecha:** 25 de noviembre de 2026

Este documento explica cómo publicar el dashboard. El despliegue real requiere la cuenta de GitHub y la cuenta de Streamlit del grupo; no se incluyen credenciales ni secretos.

---

## 1. Antes de empezar

Verificar que el proyecto tenga:

- `app.py` en la raíz.
- `requirements.txt` con las dependencias mínimas del dashboard.
- `runtime.txt` con `python-3.12`.
- `src/` con `config.py`, `cleaning.py`, `analysis.py`, `model.py` y `__init__.py`.
- `data/clean/` con los CSV que usa el dashboard.
- `reports/tablas/` con las tablas que usa el dashboard.
- `README.md`, `LICENSE`, `.gitignore`.

El dashboard necesita los archivos de `data/clean/` y `reports/tablas/`; no necesita los notebooks ni los PDF para funcionar.

---

## 2. Crear el repositorio en GitHub

1. Entrar a https://github.com y crear una cuenta si no existe.
2. Crear un repositorio nuevo, por ejemplo `irca-cauca`.
3. Elegir **Private** o **Public** según lo que pida el docente.
4. No marcar “Add a README” si se va a subir el proyecto completo.
5. Copiar la URL del repositorio, por ejemplo `https://github.com/usuario/irca-cauca.git`.

### Subir el proyecto desde la carpeta local

En la carpeta `electiva-profesional-ii-trabajo-final`:

```bash
git init
git add .
git commit -m "Proyecto final IRCA Cauca"
git branch -M main
git remote add origin https://github.com/usuario/irca-cauca.git
git push -u origin main
```

Si GitHub pide autenticación, usar un *personal access token* o el flujo del navegador. No subir contraseñas ni tokens al repositorio.

> El `.gitignore` excluye `.venv/`, `__pycache__/`, `.env` y `.streamlit/secrets.toml`.

---

## 3. Desplegar en Streamlit Community Cloud

1. Entrar a https://share.streamlit.io.
2. Iniciar sesión con **GitHub** (usar la misma cuenta del repositorio).
3. Hacer clic en **New app**.
4. Seleccionar:
   - **Repository:** `usuario/irca-cauca`.
   - **Branch:** `main`.
   - **Main file path:** `app.py`.
5. En **Python version**, elegir **3.12** (debe coincidir con `runtime.txt`).
6. Hacer clic en **Deploy**.
7. Esperar a que termine la instalación de `requirements.txt` y el arranque de la app.
8. Copiar la URL pública, por ejemplo `https://irca-cauca-usuario.streamlit.app`.

### Comprobar el despliegue

- [ ] La app abre sin pantalla de error.
- [ ] Las cuatro pestañas cargan.
- [ ] Los filtros funcionan.
- [ ] Las descargas CSV funcionan.
- [ ] La URL se abre en una ventana de incógnito (para descartar caché).
- [ ] La URL se anota en `README.md` y en `video/guion_video.md`.

---

## 4. Actualizar el README

Reemplazar en `README.md`:

```markdown
> **Dashboard publicado:** _completar la URL de Streamlit Community Cloud después del despliegue._
> **Repositorio:** _completar la URL de GitHub después de publicar._
```

por las URLs reales. Hacer `git add`, `git commit` y `git push` para que el repositorio quede actualizado.

---

## 5. Solución de problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'src'` | Streamlit Cloud no encuentra el paquete. | Confirmar que `src/__init__.py` existe y que `app.py` inserta la raíz en `sys.path`. |
| `ModuleNotFoundError: No module named 'pandas'` | `requirements.txt` no se leyó. | Verificar que el archivo esté en la raíz y que la app apunte a `app.py`. |
| La app se queda cargando | El arranque tardó o hubo un error en el log. | Abrir **Manage app → Logs** y revisar el error. |
| `FileNotFoundError` de un CSV | Falta un archivo en el repositorio. | Confirmar que `data/clean/` y `reports/tablas/` se subieron. |
| Error de versión de Python | `runtime.txt` no coincide con la versión elegida. | Usar `python-3.12` en ambos. |
| La app “duerme” tras inactividad | Comportamiento normal del plan gratuito. | Abrir la URL para despertarla; no afecta la entrega. |
| Cambios no aparecen | GitHub no recibió el último commit. | Hacer `git push`; Streamlit Cloud redespliega automáticamente. |

### Revisar logs

En Streamlit Community Cloud:

1. Abrir el panel de la app.
2. Hacer clic en **Manage app**.
3. Revisar **Logs**.
4. Buscar el primer error; normalmente indica el archivo o la dependencia que falta.

---

## 6. Buenas prácticas de seguridad

- No subir `.env`, credenciales, tokens ni `secrets.toml`.
- No incluir datos personales; el IRCA es agregado.
- Mantener el repositorio privado si el docente lo permite; la URL del dashboard puede compartirse.
- Revisar que el repositorio no contenga archivos temporales (`_test_*.png`, `__pycache__/`).

---

## 7. Checklist final de despliegue

- [ ] Repositorio GitHub creado y con el último commit.
- [ ] `requirements.txt` y `runtime.txt` en la raíz.
- [ ] `app.py` desplegado sin errores.
- [ ] URL pública anotada en `README.md`.
- [ ] Captura del dashboard desplegado guardada en `reports/capturas/` o en el video.
- [ ] Prueba en incógnito realizada.
- [ ] Repositorio sin secretos.