from typing import Annotated

from typer import Argument, Option

from preling.app.app import app

__all__ = [
    'delete',
]


@app.command()
def delete(
        language: Annotated[
            str,
            Argument(help='Language code whose data should be removed.'),
        ],
        force: Annotated[
            bool | None,
            Option(
                '--force',
                '-f',
                help='Skip the confirmation prompt and delete immediately.',
            ),
        ] = False,
) -> None:
    """Delete all stored data for `language`."""
    print(f'Deleting data for language "{language}"/{force}...')
