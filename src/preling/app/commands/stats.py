from typing import Annotated

from typer import Argument

from preling.app.app import app

__all__ = [
    'stats',
]


@app.command()
def stats(
        language: Annotated[
            str,
            Argument(help='Language code to show study statistics for.'),
        ],
) -> None:
    """Display study statistics for language."""
    print(f'Displaying study statistics for language {language}...')
