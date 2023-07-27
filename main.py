from pathlib import Path

import logzero
import typer

import settings
from lib.render import TemplateEngine
from lib.repository import StudentRepository
from lib.utils import init_logger

logger = init_logger()

app = typer.Typer(add_completion=False)


@app.command()
def run(
    loglevel: str = typer.Option(
        'DEBUG', '--loglevel', '-l', help='Log level (debug, info, error)'
    ),
    group: list[str] = typer.Option([], '--group', '-g', help='Filtrar por grupo.'),
    cial: list[str] = typer.Option([], '--cial', '-c', help='Filtrar por CIAL.'),
    exp: list[str] = typer.Option([], '--exp', '-e', help='Filtrar por expediente.'),
    id: list[str] = typer.Option([], '--id', '-i', help='Filtrar por DNI/NIF/NIE.'),
    gender: list[str] = typer.Option(
        [], '--gender', '-n', help='Filtrar por género [V=Varón/M=Mujer]'
    ),
    adult: bool = typer.Option(
        None, '--adult/--no-adult', '-d/-D', help='Filtrar por adulto/no adulto.'
    ),
    shift: list[str] = typer.Option(
        [], '--shift', '-h', help='Filtrar por turno [M=Mañana/T=Tarde/N=Noche]'
    ),
    active: bool = typer.Option(
        None, '--active/--no-active', '-a/-A', help='Filtrar por activo/dado de baja.'
    ),
    has_pic: bool = typer.Option(
        None, '--pic/--no-pic', '-p/-P', help='Filtrar por si tiene foto o no.'
    ),
    sort_by: list[str] = typer.Option(
        ['group', 'list_number', 'surname'], '--sort-by', '-s', help='Ordenar por campos.'
    ),
    input_path: Path = typer.Option(
        settings.STUDENTS_DATA_PATH,
        '--input',
        '-i',
        help='Ruta al fichero de datos de entrada (.csv)',
    ),
    output_path: Path = typer.Option(
        settings.CARDS_OUTPUT_PATH,
        '--output',
        '-o',
        help='Ruta al fichero de tarjetas de salida (.pdf)',
    ),
    pics_dir: Path = typer.Option(
        settings.PROFILE_PICS_DIR,
        '--pics-dir',
        '-r',
        help='Ruta al directorio donde se encuentran las fotos de perfil.',
    ),
):
    '''Generador de tarjetas'''
    logger.setLevel(getattr(logzero, loglevel.upper()))

    students = StudentRepository(data_path=input_path, pics_dir=pics_dir)
    filtered_students = students.filter(
        group=group,
        cial=cial,
        exp=exp,
        id=id,
        gender=gender,
        adult=adult,
        short_shift=shift,
        active=active,
        has_pic=has_pic,
    ).sort(*sort_by)
    filtered_students.check()
    tengine = TemplateEngine(project_dir=settings.PROJECT_DIR, school_year=settings.SCHOOL_YEAR)
    tengine.render(students=filtered_students, output_path=output_path)


if __name__ == "__main__":
    app()
