import typer

import settings
from lib.render import TemplateEngine
from lib.repository import StudentRepository

app = typer.Typer(add_completion=False)


@app.command()
def run(
    group: list[str] = typer.Option([], '--group', '-g', help='Filter by group'),
    cial: list[str] = typer.Option([], '--cial', '-c', help='Filter by CIAL'),
    exp: list[str] = typer.Option([], '--exp', '-e', help='Filter by expedient'),
    id: list[str] = typer.Option([], '--id', '-i', help='Filter by DNI/NIF/NIE'),
    gender: list[str] = typer.Option([], '--gender', '-n', help='Filter by gender [V/M]'),
    adult: bool = typer.Option(None, '--adult/--underage', '-a/-U', help='Filter by age status'),
    shift: list[str] = typer.Option([], '--shift', '-h', help='Filter by shift [M/T/N]'),
    sort_by: list[str] = typer.Option(
        ['group', 'list_number', 'fullname'], '--sort-by', '-s', help='Sort by fields'
    ),
):
    '''Make cards'''
    students = StudentRepository()
    tengine = TemplateEngine(project_dir=settings.PROJECT_DIR, school_year=settings.SCHOOL_YEAR)
    filtered_students = students.filter(
        group=group, cial=cial, exp=exp, id=id, gender=gender, adult=adult, short_shift=shift
    ).sort(*sort_by)
    tengine.render(students=filtered_students)


if __name__ == "__main__":
    app()
