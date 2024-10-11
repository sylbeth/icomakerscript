from PIL import Image
from utils import path_to_all_images, get_arguments, get_sizes

def convert_png_to_ico(path: str, sizes: list[tuple[int, int]]) -> None:
    """
    Converts the png from the given path to an ico.

    Parameters
    __________
    path: [:class:`str`]
        Path to the png to convert.
    sizes: [:class:`list[tuple[int, int]]`]
        Sizes that the original png will be resized to ensemble the ico.
    """
    image = Image.open(path)
    image.save(f'{path[:-3]}ico', sizes=sizes)
    print(path, "converted.")

def process() -> None:
    """
    Processes the conversion.
    """
    arguments: Namespace = get_arguments()
    if not arguments.force_reconversion:
        already_made: set[str] = {f'{path[:-3]}png' for path in path_to_all_images(arguments.directory, 'ico')}
    _, sizes = get_sizes(arguments)
    for path in path_to_all_images(arguments.directory, 'png'):
        if arguments.force_reconversion or \
            (path not in already_made and \
                (arguments.enable_name_with_dot_as_png or \
                    path.split('\\')[-1][:-4].find('.') == -1)):
            convert_png_to_ico(path, sizes)

if __name__ == '__main__':
    process()
