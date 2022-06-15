import click
import os


@click.group(invoke_without_command=True)
def main():
    pass


@main.command()
@click.argument("message", default="migration")
def makemigrations(message):
    os.system(f"alembic revision --autogenerate -m \"{message}\"")


@main.command()
def migrate():
    os.system("alembic upgrade head")


@main.command()
def makerequirements():
    os.system("pipenv lock -r > requirements.txt")


if __name__ == '__main__':
    main()
