# 🗂️ genera_tarjetas

Herramienta para generar tarjetas del alumnado del [IES Puerto de la Cruz - Telesforo Bravo](http://iespto.es).

## Requisitos previos

1. [Python >= 3.10](https://www.python.org/downloads/)
2. [Prince](https://www.princexml.com/download/)

## Configuración

1. Descargar el proyecto y entrar en la carpeta `genera_tarjetas`.

2. Crear un entorno virtual:

```console
python -m venv .venv --prompt genera_tarjetas
```

3. Activar el entorno virtual:

| Linux                       | Windows                    |
| --------------------------- | -------------------------- |
| `source .venv/bin/activate` | `".venv/Scripts/activate"` |

4. Instalar las dependencias:

```console
pip install -r requirements.txt
```

5. Si el ejecutable `prince` no está en el path, crear un fichero `.env` en el raíz del proyecto indicando la ruta completa al ejecutable.

   Por ejemplo, si estamos en Windows deberíamos definir algo como:

   `PRINCE_PATH=C:\Program Files (x86)\Prince\engine\bin\prince`

## Modo de uso

```
Usage: main.py [OPTIONS]

  Generador de tarjetas

Options:
  -l, --loglevel TEXT             Log level (debug, info, error)  [default:
                                  DEBUG]
  -g, --group TEXT                Filtrar por grupo.
  -c, --cial TEXT                 Filtrar por CIAL.
  -e, --exp TEXT                  Filtrar por expediente.
  -i, --id TEXT                   Filtrar por DNI/NIF/NIE.
  -n, --gender TEXT               Filtrar por género [V=Varón/M=Mujer]
  -d, --adult / -D, --no-adult    Filtrar por adulto/no adulto.
  -h, --shift TEXT                Filtrar por turno [M=Mañana/T=Tarde/N=Noche]
  -a, --active / -A, --no-active  Filtrar por activo/dado de baja.
  -p, --pic / -P, --no-pic        Filtrar por si tiene foto o no.
  -f, --adult-ref-date TEXT       El alumnado se considerará adulto si el día
                                  que cumpla 18 años está comprendido entre
                                  este valor y la fecha de hoy.  [default:
                                  1900-01-01]
  -s, --sort-by TEXT              Ordenar por campos.  [default: group,
                                  list_number, surname]
  -i, --input PATH                Ruta al fichero de datos de entrada (.csv)
                                  [default: /Users/sdelquin/code/iespuertodela
                                  cruz/genera_tarjetas/data/students.csv]
  -o, --output PATH               Ruta al fichero de tarjetas de salida (.pdf)
                                  [default: /Users/sdelquin/code/iespuertodela
                                  cruz/genera_tarjetas/output/cards.pdf]
  -r, --pics-dir PATH             Ruta al directorio donde se encuentran las
                                  fotos de perfil.  [default: /Users/sdelquin/
                                  code/iespuertodelacruz/genera_tarjetas/data/
                                  pics]
  --help                          Show this message and exit.
```
