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
    os.system(f"alembic upgrade head")


if __name__ == '__main__':
    main()
