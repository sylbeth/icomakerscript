from subprocess import check_call, check_output
from argparse import Namespace
from PIL.Image import open as image_open
from PIL.ImageFile import ImageFile
from utils import path_to_all_images, get_arguments, get_sizes

def convert_svg_to_ico(path: str, str_sizes: list[str], tuple_sizes: list[tuple[int, int]]) -> None:
    """
    Converts the svg from the given path to an ico.

    Parameters
    __________
    path: [:class:`str`]
        Path to the svg to convert.
    str_sizes: [:class:`list[str]`]
        List of the sizes to convert the svg to.
    tuple_sizes: [:class:`list[tuple[int,int]]`]
        List of the dimensions of the images that will form the ico.
    """
    convert_svg_to_pngs(path, str_sizes)
    convert_pngs_to_ico(path, str_sizes, tuple_sizes)
    print(path, "converted.")

def convert_svg_to_pngs(path: str, str_sizes: list[str]) -> None:
    """
    Converts the svg from the given path to a batch of pngs of different sizes.

    Parameters
    __________
    path: [:class:`str`]
        Path to the svg to convert.
    str_sizes: [:class:`list[str]`]
        List of the sizes to convert the svg to.
    """
    for size in str_sizes:
        check_call([
            'inkscape',
            '--export-area-page',
            f'--export-filename={path[:-3]}{size}.png',
            '--export-type=png',
            '-w', size,
            '-h', size,
            path
        ])

def convert_pngs_to_ico(path: str,  str_sizes: list[str], tuple_sizes: list[tuple[int, int]]) -> None:
    """
    Converts the pngs (previously converted from a svg) from the given path to an ico.

    Parameters
    __________
    path: [:class:`str`]
        Path to the original svg to convert.
    str_sizes: [:class:`list[str]`]
        List of the sizes that the svg has been converted to.
    tuple_sizes: [:class:`list[tuple[int,int]]`]
        List of the dimensions of the images that will form the ico.
    """
    paths: list[str] = [f'{path[:-3]}{size}.png' for size in str_sizes]
    images: list[ImageFile] = [image_open(path) for path in paths]
    images[-1].save(f'{path[:-3]}ico', sizes=tuple_sizes, append_images=images)

def process() -> None:
    """
    Processes the conversion.
    """
    arguments: Namespace = get_arguments()
    if not arguments.force_reconversion:
        already_made: set[str] = {f'{path[:-3]}svg' for path in path_to_all_images(arguments.directory, 'ico')}
    str_sizes, tuple_sizes = get_sizes(arguments)
    for path in path_to_all_images(arguments.directory, 'svg'):
        if arguments.force_reconversion or path not in already_made:
            convert_svg_to_ico(path, str_sizes, tuple_sizes)

if __name__ == '__main__':
    process()
