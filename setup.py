#!/usr/bin/env python
from setuptools import setup


entry_points = {
    "console_scripts": [
        "simulate_ecs_run = acispy_cmd.simulate_ecs_run:main",
        "plot_msid = acispy_cmd.plot_msid:main",
        "current_load_page = acispy_cmd.current_load_page:main",
        "dpa_temperature_plots = acispy_cmd.dpa_temperature_plots:main",
        "make_sop_table = acispy_cmd.make_sop_table:main",
        "multiplot_archive = acispy_cmd.multiplot_archive:main",
        "multiplot_tracelog = acispy_cmd.multiplot_tracelog:main",
        "phase_histogram_plot = acispy_cmd.phase_histogram_plot:main",
        "phase_scatter_plot = acispy_cmd.phase_scatter_plot:main",
        "plot_10day_tl = acispy_cmd.plot_10day_tl:main",
        "plot_model = acispy_cmd.plot_model:main",
    ],
}

setup(name='acispy_cmd',
      packages=['acispy_cmd'],
      use_scm_version=True,
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      description='Python-based command-line tools for ACIS Ops',
      author='John ZuHone',
      author_email='john.zuhone@cfa.harvard.edu',
      url='http://github.com/acisops/acispy_cmd',
      install_requires=["numpy>=1.12.1","requests","astropy"],
      classifiers=[
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3'
      ],
      entry_points=entry_points,
      )
