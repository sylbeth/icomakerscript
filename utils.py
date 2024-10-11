from pathlib import Path
from argparse import ArgumentParser, Namespace

str_sizes: list[str] = ['16', '24', '32', '48', '64', '96', '128', '256']
"""Default sizes when none are passed as arguments (stored as strings)."""

tuple_sizes: list[tuple[int, int]] = [
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (96, 96),
    (128, 128),
    (256, 256)
]
"""Default sizes when none are passed as arguments (stored as a tuple)."""

def path_to_all_images(base_directory: str, extension: str) -> list[str]:
    """
    Retrieves the path to all images with the given extension.

    Parameters
    __________
    base_directory: [:class:`str`]
        Relative directory used as the base for the search.
    extension: [:class:`str`]
        Extension of the images to search. e.g. 'svg'.
    
    Returns
    __________
    [:class:`list[str]`]
        List of the paths to all the images found.
    """
    return [str(path) for path in Path(base_directory).rglob(f'*.{extension}')]

def get_arguments() -> Namespace:
    """
    Retrieves the arguments when calling any of the scripts.

    Returns
    __________
    [:class:`Namespace`]
        Arguments used when calling the program.
    """
    argument_parser = ArgumentParser(
        prog='IcoMakerScript',
        description='Scripts that convert and generate ico files from images.'
    )
    argument_parser.add_argument(
        '-d',
        '--directory',
        default='.\\',
        help="The relative path to the directory where the images to be converted will be searched from. Defaults to the folder the script is being executed from."
        )
    argument_parser.add_argument(
        '-s',
        '--sizes',
        default='',
        help="A list of the sizes (only the width, since the icons are to be squares) that will be used to make the ico. The format is as follows: size1[,size2,...sizen]. Defaults to 16,24,32,48,64,96,128,256."
        )
    argument_parser.add_argument(
        '-f',
        '--force-reconversion',
        action='store_true',
        help="Whether you wish to force the conversion of those files that have already become icos."
        )
    argument_parser.add_argument(
        '-p',
        '--enable-name-with-dot-as-png',
        action='store_true',
        help="Only usable in png_to_ico. For compatibility with svg_to_ico, images with a . in their name will be skipped in the conversion. Enable this flag to override this, but be careful and only use it in folders where there are no png byproducts of svg_to_ico."
        )
    return argument_parser.parse_args()

def get_sizes(arguments: Namespace) -> tuple[list[str], list[tuple[int,int]]]:
    """
    Retrieves the sizes given when calling any of the scripts.

    Returns
    __________
    [:class:`list[str]`]
        Sizes for the pngs in the ico as a list of strings.
    [:class:`list[tuple[int,int]]`]
        Sizes for the pngs in the ico as a list of the dimensions.
    """
    if arguments.sizes == '':
        return str_sizes, tuple_sizes
    else:
        _str_sizes = arguments.sizes.split(',')
        return _str_sizes, [(int(size),int(size)) for size in _str_sizes]
