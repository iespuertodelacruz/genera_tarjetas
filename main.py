import datetime
from pathlib import Path

import logzero
import typer

import settings
from lib.render import TemplateEngine
from lib.repository import StudentRepository
from lib.utils import get_school_year, init_logger

logger = init_logger()

app = typer.Typer(add_completion=False)


@app.command()
def run(
    loglevel: str = typer.Option(
        'DEBUG', '--loglevel', '-l', help='Log level (debug, info, error)'
    ),
    school_year=typer.Option(
        get_school_year,
        '--school-year',
        '-y',
        help='Curso escolar. Calcula automáticamente el curso escolar actual.',
    ),
    group: list[str] = typer.Option([], '--group', '-g', help='Filtrar por grupo.'),
    cial: list[str] = typer.Option([], '--cial', '-c', help='Filtrar por CIAL.'),
    exp: list[str] = typer.Option([], '--exp', '-e', help='Filtrar por expediente.'),
    id: list[str] = typer.Option([], '--id', '-i', help='Filtrar por DNI/NIF/NIE.'),
    gender: list[str] = typer.Option(
        [], '--gender', '-n', help='Filtrar por género [V=Varón/M=Mujer]'
    ),
    adult: bool = typer.Option(
        None,
        '--adult/--no-adult',
        '-d/-D',
        help='Filtrar por adulto/no adulto.',
        show_default=False,
    ),
    shift: list[str] = typer.Option(
        [], '--shift', '-h', help='Filtrar por turno [M=Mañana/T=Tarde/N=Noche]'
    ),
    active: bool = typer.Option(
        None,
        '--active/--no-active',
        '-a/-A',
        help='Filtrar por activo/dado de baja.',
        show_default=False,
    ),
    has_pic: bool = typer.Option(
        None, '--pic/--no-pic', '-p/-P', help='Filtrar por si tiene foto o no.', show_default=False
    ),
    newer_pic_than: str = typer.Option(
        settings.EPOCH_DATE.strftime('%d-%m-%Y'),
        '--newer-pic-than',
        '-w',
        help='Sólo se tendrá en cuenta el alumnado cuya fecha de modificación de su fotografía personal sea mayor o igual que este valor. [FORMATO: dd-mm-YYYY]',
        callback=lambda v: datetime.datetime.strptime(v, '%d-%m-%Y').date(),
    ),
    adult_ref_date: str = typer.Option(
        settings.EPOCH_DATE.strftime('%d-%m-%Y'),
        '--adult-ref-date',
        '-f',
        help='El alumnado se considerará adulto si el día que cumpla 18 años está comprendido entre este valor y la fecha de hoy. [FORMATO: dd-mm-YYYY]',
        callback=lambda v: datetime.datetime.strptime(v, '%d-%m-%Y').date(),
    ),
    sort_by: list[str] = typer.Option(
        ['group', 'list_number', 'surname'], '--sort-by', '-s', help='Ordenar por campos.'
    ),
    as_list: bool = typer.Option(
        False, '--as-list', '-t', help='Volcar listado de alumnado en vez de tarjetas.'
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
    """Generador de tarjetas"""
    logger.setLevel(getattr(logzero, loglevel.upper()))

    students = StudentRepository(
        data_path=input_path,
        pics_dir=pics_dir,
        adult_ref_date=adult_ref_date,  # type: ignore
    )
    filtered_students = (
        students.query.filter_equals(
            group=group,
            cial=cial,
            exp=exp,
            id=id,
            gender=gender,
            adult=adult,
            short_shift=shift,
            active=active,
            has_pic=has_pic,
        )
        .filter_gte(pic_mod=newer_pic_than)
        .sorted(*sort_by)
    )
    filtered_students.check()
    tengine = TemplateEngine(school_year=school_year)
    template_name = settings.LIST_TEMPLATE_NAME if as_list else settings.CARDS_TEMPLATE_NAME
    if as_list and output_path == settings.CARDS_OUTPUT_PATH:
        output_path = settings.LIST_OUTPUT_PATH
    tengine.render(template_name=template_name, output_path=output_path, students=filtered_students)


if __name__ == '__main__':
    app()
