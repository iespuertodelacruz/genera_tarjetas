import typer

import settings
from lib.render import TemplateEngine
from lib.repository import StudentRepository

app = typer.Typer(add_completion=False)


@app.command()
def run(
    group: list[str] = typer.Option([], '--group', '-g', help='Filtrar por grupo'),
    cial: list[str] = typer.Option([], '--cial', '-c', help='Filtrar por CIAL'),
    exp: list[str] = typer.Option([], '--exp', '-e', help='Filtrar por expediente'),
    id: list[str] = typer.Option([], '--id', '-i', help='Filtrar por DNI/NIF/NIE'),
    gender: list[str] = typer.Option([], '--gender', '-n', help='Filtrar por género [V/M]'),
    adult: bool = typer.Option(
        None, '--adult/--no-adult', '-d/-D', help='Filtrar por adulto/no adulto'
    ),
    shift: list[str] = typer.Option([], '--shift', '-h', help='Filtrar por turno [M/T/N]'),
    active: bool = typer.Option(
        None, '--active/--no-active', '-a/-A', help='Filtrar por activo/dado de baja'
    ),
    sort_by: list[str] = typer.Option(
        ['group', 'list_number', 'surname'], '--sort-by', '-s', help='Ordenar por campos'
    ),
):
    '''Generador de tarjetas'''
    students = StudentRepository()
    tengine = TemplateEngine(project_dir=settings.PROJECT_DIR, school_year=settings.SCHOOL_YEAR)
    filtered_students = students.filter(
        group=group,
        cial=cial,
        exp=exp,
        id=id,
        gender=gender,
        adult=adult,
        short_shift=shift,
        active=active,
    ).sort(*sort_by)
    tengine.render(students=filtered_students)


if __name__ == "__main__":
    app()
