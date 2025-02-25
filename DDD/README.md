# Entrega Semana 2
Documento Compilado: https://github.com/elle184/SaludTechDeLosAlpes-Error404/blob/master/Documento%20Entrega-001-ArquitecturaDominio.pdf

---

# SaludTechDeLosAlpes-Error404
Este repositorio (**SaludTechDeLosAlpes-Error404**, rama `master`) contiene la definición y el modelado de un dominio para un sistema relacionado con el ámbito de la salud (**"SaludTech"**).  
La nomenclatura **"AS-IS"** indica que se está capturando la situación o arquitectura actual del dominio antes de realizar refactorizaciones o mejoras.

---

# Estructura del Proyecto

## `.gradle/`
Carpeta que almacena archivos y configuraciones generadas por Gradle (el sistema de construcción que se está usando).  
Suele contener metadatos o cachés que facilitan la compilación y ejecución del proyecto.

## `build.gradle`
Archivo principal de configuración de Gradle.  
Define dependencias, plugins y tareas necesarias para compilar y ejecutar el proyecto.

## `gitpod.Dockerfile` y `gitpod.yml`
Archivos de configuración para Gitpod, una plataforma que permite desarrollar el proyecto en un entorno de contenedor.  
Contienen la definición del ambiente (`Dockerfile`) y las instrucciones de inicialización (`gitpod.yml`) para preparar el workspace.

## `src/main/cml/domain/`
Directorio que contiene los archivos escritos en **Context Mapping Language (CML)**.  

- **`SaludTechContext.cml`** y **`SaludTechContext_AS-IS.cml`**: Definen el modelado de dominios y subdominios, así como la representación de **Bounded Contexts** en el estado actual (“AS-IS”).
- **`processing-image.cml`**: Describe posibles ajustes o cambios (como la modificación de nombres de subdominios) dentro del dominio modelado.

## `README.md`
Archivo de documentación inicial (commit **"Initial commit"**).  
Normalmente describe el propósito del proyecto, cómo configurarlo y ejecutar su contenido, pero aún no tiene mayor contenido según la imagen (**"Initial commit"**).


