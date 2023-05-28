from typing import Optional, Union, Iterable

import numpy as np

from metadrive.obs.top_down_renderer import draw_top_down_map as native_draw
from metadrive.utils.utils import import_pygame

pygame = import_pygame()


def draw_top_down_map(map, reference_line=None, reference_line_width=4, resolution: Iterable = (512, 512)) -> Optional[
    Union[np.ndarray, pygame.Surface]]:
    return native_draw(map,
                       resolution,
                       reference_line=reference_line,
                       reference_line_width=reference_line_width,
                       return_surface=False)
