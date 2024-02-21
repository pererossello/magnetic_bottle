import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

class Figure:
    def __init__(self, fig_size=540, ratio=2, dpi=300, subplots=(1, 1),
                 width_ratios=None, height_ratios=None, 
                 hspace=None, wspace=None,
                 ts=1.7, pad=0.2, sw=0.2,
                 minor_ticks=True,
                 theme='dark', color=None, ax_color=None,
                 grid=True):

        fig_width, fig_height = fig_size * ratio / dpi, fig_size / dpi
        fs = np.sqrt(fig_width * fig_height)

        self.fs = fs
        self.fig_size = fig_size
        self.ratio = ratio
        self.fig_width = fig_width
        self.fig_height = fig_height
        self.subplots = subplots
        self.width_ratios = width_ratios
        self.height_ratios = height_ratios
        self.hspace = hspace
        self.wspace = wspace
        self.ts = ts
        self.sw = sw
        self.pad = pad
        self.minor_ticks = minor_ticks
        self.grid = grid

        self.fig = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
        self.dpi = dpi

        # theme can only be dark or default, make a raiserror
        if not theme in ['dark', 'default']:
            raise ValueError('Theme must be "dark" or "default".')

        self.theme = theme  # This is set but not used in your provided code
        if theme == "dark":
            self.color = '#222222'
            self.ax_color = 'w'
            self.fig.patch.set_facecolor(self.color)
            plt.rcParams.update({"text.color": "white"})
        else:
            self.color = 'w'
            self.ax_color = 'k'
            plt.rcParams.update({"text.color": "k"})

        if color is not None:
            self.color = color
            self.fig.patch.set_facecolor(self.color)
        if ax_color is not None:
            self.ax_color = ax_color
            plt.rcParams.update({"text.color": ax_color})

        # GridSpec setup
        gs = mpl.gridspec.GridSpec(
            nrows=subplots[0], ncols=subplots[1], figure=self.fig,
            width_ratios=width_ratios or [1] * subplots[1],
            height_ratios=height_ratios or [1] * subplots[0],
            hspace=hspace, wspace=wspace
        )

        # Creating subplots
        self.axes = []
        for i in range(subplots[0]):
            row_axes = []
            for j in range(subplots[1]):
                ax = self.fig.add_subplot(gs[i, j])
                row_axes.append(ax)
            self.axes.append(row_axes)

        for i in range(subplots[0]):
            for j in range(subplots[1]):
                ax = self.axes[i][j]

                ax.set_facecolor(self.color)

                for spine in ax.spines.values():
                    spine.set_linewidth(fs * sw)
                    spine.set_color(self.ax_color)

                if grid:

                    ax.grid(
                        which="major",
                        linewidth=fs * sw*0.5,
                        color=self.ax_color,
                        alpha=0.25
                    )

                ax.tick_params(
                    axis="both",
                    which="major",
                    labelsize=ts * fs,
                    size=fs * sw*5,
                    width=fs * sw*0.9,
                    pad= pad * fs,
                    top=True,
                    right=True,
                    labelbottom=True,
                    labeltop=False,
                    direction='inout',
                    color=self.ax_color,
                    labelcolor=self.ax_color
                )

                if minor_ticks == True:
                    ax.minorticks_on()

                    ax.tick_params(axis='both', which="minor", 
                    direction='inout',
                    top=True,
                    right=True,
                    size=fs * sw*2.5, 
                    width=fs * sw*0.8,
                    color=self.ax_color)

        self.axes_flat = [ax for row in self.axes for ax in row]


    def customize_axes(self, ax, ylabel_pos='left', 
                       xlabel_pos='bottom',):

        if ylabel_pos == 'left':
            labelright_bool = False
            labelleft_bool = True
        elif ylabel_pos == 'right':
            labelright_bool = True
            labelleft_bool = False

        if xlabel_pos == 'bottom':
            labeltop_bool = False
            labelbottom_bool = True
        elif xlabel_pos == 'top':
            labeltop_bool = True
            labelbottom_bool = False
        

        ax.tick_params(
            axis="both",
            which="major",
            labelsize=self.ts * self.fs,
            size=self.fs * self.sw*5,
            width=self.fs * self.sw*0.9,
            pad= self.pad * self.fs,
            top=True,
            right=True,
            labelbottom=labelbottom_bool,
            labeltop=labeltop_bool,
            labelright=labelright_bool,
            labelleft=labelleft_bool,
            direction='inout',
            color=self.ax_color,
            labelcolor=self.ax_color
        )

        if self.minor_ticks == True:
            ax.minorticks_on()

            ax.tick_params(axis='both', which="minor", 
            direction='inout',
            top=True,
            right=True,
            size=self.fs * self.sw*2.5, 
            width=self.fs * self.sw*0.8,
            color=self.ax_color)

        ax.set_facecolor(self.color)

        for spine in ax.spines.values():
            spine.set_linewidth(self.fs * self.sw)
            spine.set_color(self.ax_color)

        if self.grid:

            ax.grid(
                which="major",
                linewidth=self.fs * self.sw*0.5,
                color=self.ax_color,
                alpha=0.25
            )

        return ax


    def save(self, path, bbox_inches=None, pad_inches=None):

        self.fig.savefig(path, dpi=self.dpi, bbox_inches=bbox_inches, pad_inches=pad_inches)

        self.path = path

        

class Figure3D:
    def __init__(self, fig_size=540, ratio=2, dpi=300,
                 ts=1.7, pad=0.2, sw=0.2, 
                 pad_color='#454545', 
                 color='k', ax_color='w',
                 azimuth=25, polar=45,
                 lims=1, show=True):

        fig_width, fig_height = fig_size * ratio / dpi, fig_size / dpi
        fs = np.sqrt(fig_width * fig_height)

        self.fs = fs
        self.fig_size = fig_size
        self.ratio = ratio
        self.fig_width = fig_width
        self.fig_height = fig_height
        self.ts = ts
        self.sw = sw
        self.pad = pad
        self.dpi = dpi
        self.color = color
        self.ax_color = ax_color
        self.pad_color = pad_color

        self.show = show

        self.fig = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)

        self.fig.patch.set_facecolor(pad_color)

        ax = self.fig.add_subplot(111, projection='3d')
        self.ax = ax
    
        ax.view_init(elev=azimuth, azim=polar)

        ax.set_facecolor(color)
        
        if isinstance(lims, (int, float)):
            lims = [(-lims, lims)]*3
        if isinstance(lims, (list, tuple)):
            for i, lim in enumerate(lims):
                if isinstance(lim, (int, float, np.float32, np.int32)):
                    lims[i] = (-lim, lim)

        self.x_lim = lims[0]
        self.y_lim = lims[1]
        self.z_lim = lims[2]

        ax.set_xlim(self.x_lim)
        ax.set_ylim(self.y_lim)
        ax.set_zlim(self.z_lim)

        for k, axis in enumerate([ax.xaxis, ax.yaxis, ax.zaxis]):
            axis.line.set_linewidth(0 * fs)
            axis.set_visible(False)
            axis.pane.fill = False
            axis.pane.set_edgecolor('none')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        dx = lims[0][1] - lims[0][0]
        dy = lims[1][1] - lims[1][0]
        dz = lims[2][1] - lims[2][0]

        ax.set_box_aspect([1,dy/dx,dz/dx])



    def create_ticks(self, lw=0.2, positive_only=False, ax_lims=None, ax_labels=True, ax_text_pad=1.15, ls='--', alpha=1, zorder=1):

        if ax_lims == None:
            ax_lims = [self.x_lim, self.y_lim, self.z_lim]

        if isinstance(ax_lims, (int, float)):
            ax_lims = [(-ax_lims, ax_lims)]*3
        if isinstance(ax_lims, (list, tuple)):
            for i, lim in enumerate(ax_lims):
                if isinstance(lim, (int, float)):
                    ax_lims[i] = (-lim, lim) if not positive_only else (0, lim)
                if isinstance(lim, (list, tuple)):
                    if len(lim) == 2:
                        ax_lims[i] = lim if not positive_only else (0, lim[1])

        print(ax_lims)

        x_ax = (ax_lims[0], [0,0], [0,0])
        y_ax = ([0,0], ax_lims[1], [0,0])
        z_ax = ([0,0], [0,0], ax_lims[2])

        if isinstance(ax_text_pad, (int, float)):
            ax_text_pad = [ax_text_pad]*3

        if ax_labels:

            ax_names = ['X', 'Y', 'Z']
            ax_ax = [x_ax, y_ax, z_ax]
            for ax_ in ax_ax:
                self.ax.plot3D(*ax_, self.ax_color, lw=lw*self.fs, ls=ls, alpha=alpha, zorder=zorder)

            dx = ax_lims[0][1] - ax_lims[0][0]
            dy = ax_lims[1][1] - ax_lims[1][0]
            dz = ax_lims[2][1] - ax_lims[2][0]

            self.ax.text(ax_lims[0][1]*ax_text_pad[0], 0, 0, 'X', color=self.ax_color, fontsize=self.ts*self.fs, ha='center', va='center', alpha=alpha, zorder=zorder)

            self.ax.text(0, ax_lims[1][1]*ax_text_pad[1], 0, 'Y', color=self.ax_color, fontsize=self.ts*self.fs, ha='center', va='center', alpha=alpha, zorder=zorder)

            self.ax.text(0, 0, ax_lims[2][1]*ax_text_pad[2], 'Z', color=self.ax_color, fontsize=self.ts*self.fs, ha='center', va='center', alpha=alpha, zorder=zorder)




    def save(self, path, bbox_inches='tight', pad_inches=None, show=False):

        self.fig.savefig(path, dpi=self.dpi, bbox_inches=bbox_inches, pad_inches=pad_inches)

        self.path = path

        if not show:
            plt.close(self.fig)

