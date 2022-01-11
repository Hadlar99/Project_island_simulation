"""
Demo of how to create an island map with legend.
"""

import matplotlib.pyplot as plt
import textwrap



def mapping(island_map):

    island_map = textwrap.dedent(island_map)

    #                   R    G    B
    rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                 'L': (0.0, 0.6, 0.0),  # dark green
                 'H': (0.5, 1.0, 0.5),  # light green
                 'D': (1.0, 1.0, 0.5)}  # light yellow

    map_rgb = [[rgb_value[column] for column in row]
               for row in island_map.splitlines()]

    return map_rgb

"""
       fig = plt.figure()

    ax_im = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h

    ax_im.imshow(map_rgb)

    ax_im.set_xticks(range(0, len(map_rgb[0]), 5))
    ax_im.set_xticklabels(range(1, 1 + len(map_rgb[0]), 5))
    ax_im.set_yticks(range(0, len(map_rgb), 5))
    ax_im.set_yticklabels(range(1, 1 + len(map_rgb), 5))

    ax_lg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
    ax_lg.axis('off')
    for ix, name in enumerate(('Water', 'Lowland',
                               'Highland', 'Desert')):
        ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                      edgecolor='none',
                                      facecolor=rgb_value[name[0]]))
        ax_lg.text(0.35, ix * 0.2, name, transform=ax_lg.transAxes)
"""


