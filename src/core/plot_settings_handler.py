from matplotlib.ticker import StrMethodFormatter
import matplotlib.pyplot as plt
import numpy as np


def setup_ax(ax: np.ndarray, x_label: str, y_label: str, title: str):
    ax = ax[0]
    for x in ax:

        # Despine
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)

        # Switch off ticks
        x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

        # Draw horizontal axis lines
        vals = x.get_yticks()
        for tick in vals:
            x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

        # Remove title
        x.set_title(title)

        # Set x-axis label
        x.set_xlabel(x_label, labelpad=20, weight='bold', size=12)

        # Set y-axis label
        x.set_ylabel(y_label, labelpad=20, weight='bold', size=12)

        # Format y-axis label
        x.yaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))
