from typing import Annotated

from typer import Argument

from preling.app.app import app

__all__ = [
    'path',
]


@app.command()
def path(
        language: Annotated[
            str,
            Argument(help='Language code whose data file should be printed.'),
        ],
) -> None:
    """Print the absolute path to PreLing’s data file for `language`."""
    print(f'Path to data file for language "{language}": ...')
