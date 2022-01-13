"""
:mod:`randvis.graphics` provides graphics support for RandVis.

.. note::
   * This module requires the program ``ffmpeg`` or ``convert``
     available from `<https://ffmpeg.org>` and `<https://imagemagick.org>`.
   * You can also install ``ffmpeg`` using ``conda install ffmpeg``
   * You need to set the  :const:`_FFMPEG_BINARY` and :const:`_CONVERT_BINARY`
     constants below to the command required to invoke the programs
   * You need to set the :const:`_DEFAULT_FILEBASE` constant below to the
     directory and file-name start you want to use for the graphics output
     files.

"""

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os
from biosim.map import mapping

# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('../..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif


class Graphics:
    """Provides graphics support for RandVis."""

    def __init__(self, island_map, img_dir=None, img_name=None, img_fmt=None, ymax_animals=None,
                 cmax_herbi=None, cmax_carni=None, hist_specs_age=None, hist_specs_fitness = None,
                 hist_specs_weight=None):
        """
        :param img_dir: directory for image files; no images if None
        :type img_dir: str
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix
        :type img_fmt: str
        """

        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_ctr = 0
        self._img_step = 1

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._herbivore_map_ax = None
        self._herbivore_img_axis = None
        self._carnivore_map_ax = None
        self._carnivore_img_axis = None
        self._mean_ax = None
        self._herbivore_line = None
        self._carnivore_line = None
        self.island_map = island_map
        self.island_img = None
        self._ages_hist = None
        self._ages_histogram = None
        self._weights_hist = None
        self._weights_histogram = None
        self._fitness_hist = None
        self._fitness_histogram = None

        self.ymax_animals = ymax_animals
        self.cmax_herbi = cmax_herbi
        self.cmax_carni = cmax_carni
        self.hist_specs_age = hist_specs_age
        self.hist_specs_fitness = hist_specs_fitness
        self.hist_specs_weight = hist_specs_weight


    def update(self, year, num_herbivores, num_carnivores, herbivore_map, carnivore_map,
               age_herbi=None, age_carni=None, weight_herbi=None, weight_carni=None,
               fitness_herbi=None, fitness_carni=None):
        """
        Updates graphics with current data and save to file if necessary.

        :param year: current time step
        :param sys_map: current system status (2d array)
        :param sys_mean: current mean value of system
        """

        self._update_carnivore_map(carnivore_map)
        self._update_herbivore_map(herbivore_map)
        self._update_animal_graph(year, num_herbivores, num_carnivores)
        self._update_histograms(age_herbi, age_carni, weight_herbi, weight_carni, fitness_herbi, fitness_carni)
        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-6)  # pause required to pass control to GUI

        self._save_graphics(year)

    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg for MP4 and magick for GIF

        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def setup(self, final_step, img_step):
        """
        Prepare graphics.

        Call this before calling :meth:`update()` for the first time after
        the final time step has changed.

        :param final_step: last time step to be visualised (upper limit of x-axis)
        :param img_step: interval between saving image to file
        """

        self._img_step = img_step

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._herbivore_map_ax is None:
            self._herbivore_map_ax = self._fig.add_axes([0.1, 0.7, 0.35, 0.25])
            self._herbivore_map_ax.set_title('Herbivores')
            self._herbivore_img_axis = None

        if self._carnivore_map_ax is None:
            self._carnivore_map_ax = self._fig.add_axes([0.6, 0.7, 0.35, 0.25])
            self._carnivore_map_ax.set_title('Carnivores')
            self._carnivore_img_axis = None

        if self.island_img is None:
            rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                         'L': (0.0, 0.6, 0.0),  # dark green
                         'H': (0.5, 1.0, 0.5),  # light green
                         'D': (1.0, 1.0, 0.5)}  # light yellow

            map_rgb = [[rgb_value[column] for column in row]
                       for row in self.island_map.splitlines()]
            self.island_img = self._fig.add_axes([0.05, 0.35, 0.3, 0.3])
            self.island_img.set_title('Island')
            self.island_img.imshow(map_rgb)

            self.island_img.set_xticks(range(0, len(map_rgb[0]), 5))
            self.island_img.set_xticklabels(range(1, 1 + len(map_rgb[0]), 5))
            self.island_img.set_yticks(range(0, len(map_rgb), 5))
            self.island_img.set_yticklabels(range(1, 1 + len(map_rgb), 5))

            ax_lg = self._fig.add_axes([0.35, 0.35, 0.05, 0.3])  # llx, lly, w, h
            ax_lg.axis('off')
            for ix, name in enumerate(('Water', 'Lowland',
                                       'Highland', 'Desert')):
                ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.1, 0.1,
                                              edgecolor='none',
                                              facecolor=rgb_value[name[0]]))
                ax_lg.text(0.25, ix * 0.2, name, transform=ax_lg.transAxes)



        if self._ages_hist is None:
            self._ages_hist = self._fig.add_axes([0.08, 0.1, 0.2, 0.15])
            self._ages_histogram = None

        if self._weights_hist is None:
            self._weights_hist = self._fig.add_axes([0.38, 0.1, 0.2, 0.15])
            self._weights_histogram = None

        if self._fitness_hist is None:
            self._fitness_hist = self._fig.add_axes([0.70, 0.1, 0.2, 0.15])
            self._fitness_histogram = None

        # Add right subplot for line graph of mean.
        if self._mean_ax is None:
            self._mean_ax = self._fig.add_axes([0.6, 0.35, 0.35, 0.25])
            self._mean_ax.set_title('Animal population')

        # needs updating on subsequent calls to simulate()
        # add 1 so we can show values for time zero and time final_step
        self._mean_ax.set_xlim(0, final_step+1)

        if self._herbivore_line is None:
            mean_plot = self._mean_ax.plot(np.arange(0, final_step+1),
                                           np.full(final_step+1, np.nan))
            self._herbivore_line = mean_plot[0]
        else:
            x_data, y_data = self._herbivore_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step+1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._herbivore_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        if self._carnivore_line is None:
            mean_plot = self._mean_ax.plot(np.arange(0, final_step+1),
                                           np.full(final_step+1, np.nan))
            self._carnivore_line = mean_plot[0]
        else:
            x_data, y_data = self._carnivore_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step+1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._carnivore_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

    def _update_herbivore_map(self, herbivore_map):
        """Update the 2D-view of the system."""

        if self._herbivore_img_axis is not None:
            self._herbivore_img_axis.set_data(herbivore_map)
        else:
            self._herbivore_img_axis = self._herbivore_map_ax.imshow(herbivore_map,
                                                                     interpolation='nearest',
                                                                     vmin=0,
                                                                     vmax=(200 if self.cmax_herbi is None
                                                                           else self.cmax_herbi))
            plt.colorbar(self._herbivore_img_axis, ax=self._herbivore_map_ax,
                         orientation='vertical')


    def _update_carnivore_map(self, carnivore_map):
        """Update the 2D-view of the system."""

        if self._carnivore_img_axis is not None:
            self._carnivore_img_axis.set_data(carnivore_map)
        else:
            self._carnivore_img_axis = self._carnivore_map_ax.imshow(carnivore_map,
                                                                     interpolation='nearest',
                                                                     vmin=0, vmax=(60 if self.cmax_carni is None
                                                                                   else self.cmax_carni))
            plt.colorbar(self._carnivore_img_axis, ax=self._carnivore_map_ax,
                         orientation='vertical')

    def _update_animal_graph(self, step, herbivore, carnivore):
        y_data_1 = self._herbivore_line.get_ydata()
        y_data_1[step] = herbivore
        self._herbivore_line.set_ydata(y_data_1)

        y_data_2 = self._carnivore_line.get_ydata()
        y_data_2[step] = carnivore
        self._carnivore_line.set_ydata(y_data_2)
        plt.legend((self._herbivore_line, self._carnivore_line), ['Herbivore', 'Carnivore'], loc='upper left')

        if self.ymax_animals is not None:
            self._mean_ax.set_ylim(0, self.ymax_aniamls)
        else:
            self._mean_ax.set_ylim(0, herbivore+carnivore)


    def _update_histograms(self, age_herbi, age_carn, weight_herbi, weight_carn, fitness_herbi, fitness_carn):


        self._ages_hist.cla()
        self._ages_hist.set_title('Age')
        self._ages_histogram = self._ages_hist.hist(age_herbi, bins=np.arange(0, self.hist_specs_age['max']
                                                                          + self.hist_specs_age['delta'],
                                                                          self.hist_specs_age['delta']),
                                                    histtype='step')
        self._ages_histogram = self._ages_hist.hist(age_carn, bins=np.arange(0, self.hist_specs_age['max']
                                                                          + self.hist_specs_age['delta'],
                                                                          self.hist_specs_age['delta']),
                                                    histtype='step')
        self._ages_hist.legend(['Herbivore', 'Carnivore'])

        self._weights_hist.cla()
        self._weights_hist.set_title('Weights')
        self._weights_histogram = self._weights_hist.hist(weight_herbi,  bins=np.arange(0, self.hist_specs_weight['max']
                                                                          + self.hist_specs_weight['delta'],
                                                                          self.hist_specs_weight['delta']),
                                                    histtype='step')
        self._weights_histogram = self._weights_hist.hist(weight_carn, bins=np.arange(0, self.hist_specs_weight['max']
                                                                        + self.hist_specs_weight['delta'],
                                                                          self.hist_specs_weight['delta']),
                                                    histtype='step')
        self._weights_hist.legend(['Herbivore', 'Carnivore'])

        self._fitness_hist.cla()
        self._fitness_hist.set_title('Fitness')
        self._fitness_histogram = self._fitness_hist.hist(fitness_herbi,  bins=np.arange(0, self.hist_specs_fitness['max']
                                                                          + self.hist_specs_fitness['delta'],
                                                                          self.hist_specs_fitness['delta']),
                                                    histtype='step')
        self._fitness_histogram = self._fitness_hist.hist(fitness_carn,  bins=np.arange(0, self.hist_specs_fitness['max']
                                                                          + self.hist_specs_fitness['delta'],
                                                                          self.hist_specs_fitness['delta']),
                                                    histtype='step')
        self._fitness_hist.legend(['Herbivore', 'Carnivore'], loc='upper center')

    def _save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self._img_base is None or step % self._img_step != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
