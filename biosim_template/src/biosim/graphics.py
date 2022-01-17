"""
This is a modified graphic from the Randvis project to Biosim.

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

# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('../results', 'data')
_DEFAULT_GRAPHICS_NAME = 'biosim'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif


class Graphics:
    """Provides graphics support for Biosim."""

    def __init__(self, island_map, vis_years=1, img_dir=None, img_name=None, img_fmt=None,
                 ymax_animals=None, cmax_herbi=None, cmax_carni=None, hist_specs_age=None, hist_specs_fitness=None,
                 hist_specs_weight=None):
        """

        Parameters
        ----------
        island_map: string
            gives description on how the island look
        vis_years: int
            Tells how many years between each graphics update
        img_dir: string
            gives a path to where to save the graphics
        img_name: string
            gives the filename to where the graphics will be saved
        img_fmt: string
            gives the information on what format the images shall be saved in
        ymax_animals: int
            sets the y-max limit for the population graph
        cmax_herbi: dict
            sets the color code on the heatmap for herbivores
        cmax_carni: dict
            sets the color code on the heatmap for carnivores
        hist_specs_age: dict
            sets the x-max limit and the bins for the age histogram
        hist_specs_fitness: dict
            sets the x-max limit and the bins for the fitness histogram
        hist_specs_weight: dict
            sets the x-max limit and the bins for the weight histogram
        """

        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_ctr = 0
        self._img_year = 1
        self._vis_year = vis_years

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._herbivore_map_ax = None
        self._herbivore_img_axis = None
        self._carnivore_map_ax = None
        self._carnivore_img_axis = None
        self._mean_ax = None
        self._herbivore_line = None
        self._carnivore_line = None
        self._island_map = island_map
        self._island_img = None
        self._island_map_lines = self._island_map.splitlines()
        self._hight = len(self._island_map_lines)
        self._length = len(self._island_map_lines[0])
        self._ages_hist = None
        self._ages_histogram = None
        self._weights_hist = None
        self._weights_histogram = None
        self._fitness_hist = None
        self._fitness_histogram = None
        self._year_ax = None
        self._year_txt = None

        # Attributes that are changeable for the user
        self.ymax_animals = ymax_animals
        self.cmax_herbi = cmax_herbi
        self.cmax_carni = cmax_carni
        self.hist_specs_age = hist_specs_age
        self.hist_specs_fitness = hist_specs_fitness
        self.hist_specs_weight = hist_specs_weight
        self.animal_ydata = []

        self.template = 'Year: {:5d}'

    def update(self, year, num_herbivores, num_carnivores, herbivore_map, carnivore_map,
               age_herbi=None, age_carni=None, weight_herbi=None, weight_carni=None,
               fitness_herbi=None, fitness_carni=None):
        """

        Parameters
        ----------
        year: int
            The current year
        num_herbivores: int
            Total number of herbivores
        num_carnivores: int
            Total number of carnivores
        herbivore_map: list
            Nested list with how many herbivores there are in each cell
        carnivore_map: list
            Nested list with how many carnivores there are in each cell
        age_herbi: list with int
            List of ages for every herbivore
        age_carni: list with int
            List of ages for every carnivore
        weight_herbi: list with float
            List of weights for every herbivore
        weight_carni: list with float
            List of weights for every carnivore
        fitness_herbi: list with float
            List of fitness for every herbivore
        fitness_carni: list with float
            List of fitness for every carnivore


        """

        self._year_txt.set_text(self.template.format(year))
        self._update_carnivore_map(carnivore_map)
        self._update_herbivore_map(herbivore_map)
        self._update_animal_graph(year, num_herbivores, num_carnivores)
        self._update_histograms(age_herbi, age_carni, weight_herbi, weight_carni, fitness_herbi, fitness_carni)
        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-6)  # pause required to pass control to GUI

        if self._img_base is not None:
            self._save_graphics(year)

    def make_movie(self, movie_fmt=None):
        """

        Parameters
        ----------
        movie_fmt: string
            Gives information on the format the movie should be made in
            Must be mp4 or GIF
            Default: mp4
        -------

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

    def setup(self, final_step, img_year):

        """
          Prepare graphics.

          Call this before calling :meth:`update()` for the first time after
          the final time step has changed.

          Parameters
          ----------
          final_step: int
              last time step to be visualised (upper limit of x-axis)
          img_year: int
              interval between saving image to file

          """

        self._img_year = img_year

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._year_ax is None:
            self._year_ax = self._fig.add_axes([0.4, 0.8, 0.2, 0.2])  # llx, lly, w, h
            self._year_ax.axis('off')  # turn off coordinate system

            self._year_txt = self._year_ax.text(0.5, 0.5, self.template.format(0),
                                                horizontalalignment='center',
                                                verticalalignment='center',
                                                transform=self._year_ax.transAxes)

        # Makes a place to put the graphics for herbivore map
        if self._herbivore_map_ax is None:
            self._herbivore_map_ax = self._fig.add_axes([0.05, 0.3, 0.35, 0.3])
            self._herbivore_map_ax.set_title('Herbivores')
            self._herbivore_img_axis = None

            # Makes the axis correct for herbivore map
            self._herbivore_map_ax.set_xticks(range(0, self._length, 5))
            self._herbivore_map_ax.set_xticklabels(range(1, 1 + self._length, 5))
            self._herbivore_map_ax.set_yticks(range(0, self._hight, 5))
            self._herbivore_map_ax.set_yticklabels(range(1, 1 + self._hight, 5))

        # Makes a place to put the graphics for carnivore map
        if self._carnivore_map_ax is None:
            self._carnivore_map_ax = self._fig.add_axes([0.6, 0.3, 0.35, 0.3])
            self._carnivore_map_ax.set_title('Carnivores')
            self._carnivore_img_axis = None

            # Makes the axis correct for carnivore map
            self._carnivore_map_ax.set_xticks(range(0, self._length, 5))
            self._carnivore_map_ax.set_xticklabels(range(1, 1 + self._length, 5))
            self._carnivore_map_ax.set_yticks(range(0, self._hight, 5))
            self._carnivore_map_ax.set_yticklabels(range(1, 1 + self._hight, 5))

        # Makes a map of the island with different color for different terrain
        if self._island_img is None:
            rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                         'L': (0.0, 0.6, 0.0),  # dark green
                         'H': (0.5, 1.0, 0.5),  # light green
                         'D': (1.0, 1.0, 0.5)}  # light yellow

            map_rgb = [[rgb_value[column] for column in row]
                       for row in self._island_map.splitlines()]
            self._island_img = self._fig.add_axes([0.05, 0.7, 0.25, 0.25])
            self._island_img.set_title('Island')
            self._island_img.imshow(map_rgb)

            # Gives correct axis to the island map
            self._island_img.set_xticks(range(0, len(map_rgb[0]), 5))
            self._island_img.set_xticklabels(range(1, 1 + len(map_rgb[0]), 5))
            self._island_img.set_yticks(range(0, len(map_rgb), 5))
            self._island_img.set_yticklabels(range(1, 1 + len(map_rgb), 5))

            # Adds description on what terrain the different colors represent
            ax_lg = self._fig.add_axes([0.3, 0.7, 0.05, 0.3])  # llx, lly, w, h
            ax_lg.axis('off')
            for ix, name in enumerate(('Water', 'Lowland',
                                       'Highland', 'Desert')):
                ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.1, 0.1,
                                              edgecolor='none',
                                              facecolor=rgb_value[name[0]]))
                ax_lg.text(0.25, ix * 0.2, name, transform=ax_lg.transAxes)

        # Makes a histogram to put the age
        if self._ages_hist is None:
            self._ages_hist = self._fig.add_axes([0.08, 0.05, 0.2, 0.15])
            self._ages_histogram = None

        # Makes a histogram to put the weight
        if self._weights_hist is None:
            self._weights_hist = self._fig.add_axes([0.38, 0.05, 0.2, 0.15])
            self._weights_histogram = None

        # Makes a histogram to put the fitness
        if self._fitness_hist is None:
            self._fitness_hist = self._fig.add_axes([0.70, 0.05, 0.2, 0.15])
            self._fitness_histogram = None

        # Makes a graph to put the animal population
        if self._mean_ax is None:
            self._mean_ax = self._fig.add_axes([0.65, 0.7, 0.3, 0.25])
            self._mean_ax.set_title('Animal population')

        # add 1 so we can show values for time zero and time final_step
        self._mean_ax.set_xlim(0, final_step+1)

        # Gets the updated statistics to put in the graph
        if self._herbivore_line is None:
            mean_plot = self._mean_ax.plot(np.arange(0, final_step+1),
                                           np.full(final_step+1, np.nan))
            self._herbivore_line = mean_plot[0]
        else:
            x_data, y_data = self._herbivore_line.get_data()
            xtr_years = np.arange(x_data[-1] + 1, final_step + 1)
            if len(xtr_years) > 0:
                x_new = np.full(xtr_years.shape, np.nan)
                y_new = np.full(xtr_years.shape, np.nan)
                self._herbivore_line.set_data(np.hstack((x_data, x_new)),
                                              np.hstack((y_data, y_new)))

        if self._carnivore_line is None:
            mean_plot = self._mean_ax.plot(np.full(final_step+1, np.nan),
                                           np.full(final_step+1, np.nan))
            self._carnivore_line = mean_plot[0]
        else:
            x_data, y_data = self._carnivore_line.get_data()
            xtr_years = np.arange(x_data[-1] + 1, final_step+1)
            if len(xtr_years) > 0:
                x_new = np.full(xtr_years.shape, np.nan)
                y_new = np.full(xtr_years.shape, np.nan)
                self._carnivore_line.set_data(np.hstack((x_data, x_new)),
                                              np.hstack((y_data, y_new)))

    def _update_herbivore_map(self, herbivore_map):
        """
        Update the map with herbivores
        Parameters
        ----------
        herbivore_map: nested list
            How many herbivores there are in each cell

        """

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
        """
        Update the map with carnivores
        Parameters
        ----------
        carnivore_map: nested list
            How many herbivores there are in each cell

        """

        if self._carnivore_img_axis is not None:
            self._carnivore_img_axis.set_data(carnivore_map)
        else:
            self._carnivore_img_axis = self._carnivore_map_ax.imshow(carnivore_map,
                                                                     interpolation='nearest',
                                                                     vmin=0, vmax=(60 if self.cmax_carni is None
                                                                                   else self.cmax_carni))
            plt.colorbar(self._carnivore_img_axis, ax=self._carnivore_map_ax,
                         orientation='vertical')

    def _update_animal_graph(self, year, herbivore, carnivore):
        """
        Updates the graph of how many herbivores and carnivores there are on the Island

        Parameters
        ----------
        year: int
            the current year
        herbivore: int
            the total amount of herbivores
        carnivore: int
            the total amount of carnivores

        """
        step = int(year/self._vis_year)

        y_data_1 = self._herbivore_line.get_ydata()
        y_data_1[step] = herbivore
        self._herbivore_line.set_ydata(y_data_1)

        x_data_1 = self._herbivore_line.get_xdata()
        x_data_1[step] = year
        self._herbivore_line.set_xdata(x_data_1)

        y_data_2 = self._carnivore_line.get_ydata()
        y_data_2[step] = carnivore
        self._carnivore_line.set_ydata(y_data_2)

        x_data_2 = self._carnivore_line.get_xdata()
        x_data_2[step] = year
        self._carnivore_line.set_xdata(x_data_2)

        plt.legend((self._herbivore_line, self._carnivore_line), ['Herbivore', 'Carnivore'], loc='upper left')

        if self.ymax_animals is not None:
            self._mean_ax.set_ylim(0, self.ymax_animals)
        else:
            self.animal_ydata.append(max(herbivore, carnivore))
            self._mean_ax.set_ylim(0, max(self.animal_ydata))

    def _update_histograms(self, age_herbi, age_carn, weight_herbi, weight_carn, fitness_herbi, fitness_carn):
        """
        Updates all of the histograms for herbivore and carnivores on the island

        Parameters
        ----------
        age_herbi: list
            list with the age for all the herbivores
        age_carn: list
            list with the age for all the carnivores
        weight_herbi: list
            list with the weight for all the herbivores
        weight_carn: list
            list with the weight for all the carnivores
        fitness_herbi: list
            list with the fitness for all herbivores
        fitness_carn: list
            list with all fitness for all carnivores
        """

        self._ages_hist.cla()
        self._ages_hist.set_title('Age')
        if self.hist_specs_age is not None:
            self._ages_histogram = self._ages_hist.hist(age_herbi, bins=np.arange(0, self.hist_specs_age['max']
                                                                                  + self.hist_specs_age['delta'],
                                                                                  self.hist_specs_age['delta']),
                                                        histtype='step')
            self._ages_histogram = self._ages_hist.hist(age_carn, bins=np.arange(0, self.hist_specs_age['max']
                                                                                 + self.hist_specs_age['delta'],
                                                                                 self.hist_specs_age['delta']),
                                                        histtype='step')
        else:
            self._ages_histogram = self._ages_hist.hist(age_herbi, histtype='step')
            self._ages_histogram = self._ages_hist.hist(age_carn, histtype='step')

        self._weights_hist.cla()
        self._weights_hist.set_title('Weights')
        if self.hist_specs_weight is not None:
            self._weights_histogram = self._weights_hist.hist(weight_herbi,
                                                              bins=np.arange(0, self.hist_specs_weight['max']
                                                                             + self.hist_specs_weight['delta'],
                                                                             self.hist_specs_weight['delta']),
                                                              histtype='step')
            self._weights_histogram = self._weights_hist.hist(weight_carn,
                                                              bins=np.arange(0, self.hist_specs_weight['max']
                                                                             + self.hist_specs_weight['delta'],
                                                                             self.hist_specs_weight['delta']),
                                                              histtype='step')
        else:
            self._weights_histogram = self._weights_hist.hist(weight_herbi, histtype='step')
            self._weights_histogram = self._weights_hist.hist(weight_carn, histtype='step')

        self._fitness_hist.cla()
        self._fitness_hist.set_title('Fitness')
        if self.hist_specs_fitness is not None:
            self._fitness_histogram = self._fitness_hist.hist(fitness_herbi,
                                                              bins=np.arange(0, self.hist_specs_fitness['max']
                                                                             + self.hist_specs_fitness['delta'],
                                                                             self.hist_specs_fitness['delta']),
                                                              histtype='step')
            self._fitness_histogram = self._fitness_hist.hist(fitness_carn,
                                                              bins=np.arange(0, self.hist_specs_fitness['max']
                                                                             + self.hist_specs_fitness['delta'],
                                                                             self.hist_specs_fitness['delta']),
                                                              histtype='step')
        else:
            self._fitness_histogram = self._fitness_hist.hist(fitness_herbi, histtype='step')
            self._fitness_histogram = self._fitness_hist.hist(fitness_carn, histtype='step')

    def _save_graphics(self, year):
        """
        Saves graphics to file if file name given

        Parameters
        ----------
        year: int
            How many years the simulation are going to run

        Returns
        -------
        None if it does not save a figure
        """

        if self._img_base is None or year % self._img_year != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
