.. acispy_tasks documentation master file, created by
   sphinx-quickstart on Wed Jul 29 15:06:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ACISpy Command Line Tools
=========================

For making quick plots and getting quick summaries of important information, the 
following ACISpy-based command-line utilities are provided. For finer-grained 
control over plots and data, it is recommended to use the ACISpy Python interface.

Activating
----------

The ACISpy command-line tools are installed into the ACIS Ops Ska Python stack. 
If you are logged on as ``acisdude``, all you need to do is issue the 
command ``acisska`` and this Python stack and the tools will be loaded into 
your environment. 

However, if you would like activate this stack and these tools from your own user
account, add the following alias to your ``.bashrc`` if you are using the Bash
shell (or a variant):

.. code-block:: bash

    acisska () {
        PATH=/data/acis/ska/bin:$PATH
        export SKA=/proj/sot/ska
        PS1="[ska3:\u@\h \W]\$ "
    }

Or, if you are a mascohist or are otherwise compelled to use the C shell or a 
variant of it, add this alias to your ``.cshrc.user``:

.. code-block:: bash

    alias acisska 'set path = (/data/acis/ska/bin/ $path); \
	               setenv SKA /proj/sot/ska; \
	               set prompt = "[acisska] $prompt"'

.. warning::

    The ACIS Ops Ska Python stack should be used in a "clean" terminal window 
    where you are not trying to do anything else (i.e., load reviews, SACGS) 
    as setting up the Ska environment messes with environment variables and paths. 

``multiplot_archive``
---------------------

.. code-block:: text

    usage: multiplot_archive [-h] [--one-panel] [--maude] tstart tstop plots
    
    Make plots of MSIDs and commanded states from the engineering archive
    
    positional arguments:
      tstart       The start time in YYYY:DOY:HH:MM:SS format
      tstop        The stop time in YYYY:DOY:HH:MM:SS format
      plots        The MSIDs and states to plot, comma-separated
    
    optional arguments:
      -h, --help   show this help message and exit
      --one-panel  Whether to make a multi-panel plot or a single-panel plot. The
                   latter is only valid if the quantities have the same units.
      --maude      Use MAUDE to get telemetry data.

Example 1
+++++++++

.. code-block:: bash

    [~]$ multiplot_archive 2016:089 2016:091 1deamzt,1dpamzt,ccd_count
    
Returns:

.. image:: _images/multiplot_archive.png

Example 2
+++++++++

.. code-block:: bash

    [~]$ multiplot_archive 2016:091 2016:097 1pdeaat,1pdeabt,1pin1at --one-panel

.. image:: _images/one_panel_multi_archive.png

``multiplot_tracelog``
----------------------

.. code-block:: text

    usage: multiplot_tracelog [-h] [--one-panel] tracelog plots
    
    Make plots of MSIDs from a tracelog file. Commanded states will be loaded from
    the commanded states database.
    
    positional arguments:
      tracelog    The tracelog file to load the MSIDs from
      plots       The MSIDs and states to plot, comma-separated
    
    optional arguments:
      -h, --help  show this help message and exit
      --one-panel  Whether to make a multi-panel plot or a single-panel plot. The
                   latter is only valid if the quantities have the same units.

Example 1
+++++++++

.. code-block:: bash
    
    [~]$ multiplot_tracelog acisENG10d_00985114479.70.tl 1pin1at,1dp28avo,simpos
    
Returns:

.. image:: _images/multiplot_tracelog.png

Example 2
+++++++++

.. code-block:: bash
    
    [~]$ multiplot_tracelog acisENG10d_00985114479.70.tl 1dp28avo,1dp28bvo --one-panel
    
Returns:

.. image:: _images/one_panel_multi_tracelog.png

``plot_10day_tl``
-----------------

.. code-block:: text

    usage: plot_10day_tl [-h] [--days DAYS] [--one-panel] fields

    Plot one or more MSIDs or states from the ACIS 10-day tracelog files.

    positional arguments:
      fields       The MSIDs and states to plot, comma-separated

    optional arguments:
      -h, --help   show this help message and exit
      --days DAYS  The number of days before the end of the log to plot. Default:
                   10
      --one-panel  Whether to make a multi-panel plot or a single-panel plot. The
                   latter is only valid if the quantities have the same units.

Example 1
+++++++++

Plot one MSID and two states in three different panels.

.. code-block:: bash

    [~]$ plot_10day_tl 1pdeaat,pitch,off_nom_roll

Returns:

.. image:: _images/plot_10day_ex1.png

Example 2
+++++++++

Plot 3 MSIDs from ove the past three days and combine them in one panel.

.. code-block:: bash

    [~]$ plot_10day_tl 1dpamzt,tmp_fep1_mong,tmp_bep_pcb --days 3 --one-panel

Returns:

.. image:: _images/plot_10day_ex2.png

``plot_model``
--------------

.. code-block:: text

    usage: plot_model [-h] [--y2_axis Y2_AXIS] load y_axis
    
    Plot a single model component with another component or state
    
    positional arguments:
      load               The load to take the model from
      y_axis             The model component to plot on the left y-axis
    
    optional arguments:
      -h, --help         show this help message and exit
      --y2_axis Y2_AXIS  The model component or state to plot on the right y-axis
                         (default: none)

Example
+++++++

.. code-block:: bash

    [~]$ plot_model MAR0716A 1dpamzt --y2_axis=off_nom_roll
    
Returns:

.. image:: _images/plot_model.png

``plot_msid``
-------------

.. code-block:: text

    usage: plot_msid [-h] [--y2_axis Y2_AXIS] [--maude] tstart tstop y_axis
    
    Plot a single MSID with another MSID or state
    
    positional arguments:
      tstart             The start time in YYYY:DOY:HH:MM:SS format
      tstop              The stop time in YYYY:DOY:HH:MM:SS format
      y_axis             The MSID to be plotted on the left y-axis
    
    optional arguments:
      -h, --help         show this help message and exit
      --y2_axis Y2_AXIS  The MSID or state to be plotted on the right y-axis
                         (default: none)
      --maude            Use MAUDE to get telemetry data.


Example
+++++++

Plot 1PIN1AT and pitch. 

.. code-block:: bash

    [~]$ plot_msid 2016:091 2016:095 1pin1at --y2_axis=pitch

Returns:

.. image:: _images/plot_msid.png

``simulate_ecs_run``
--------------------

.. code-block:: text

   usage: simulate_ecs_run [-h] [--vehicle_load VEHICLE_LOAD] [--off_nom_roll OFF_NOM_ROLL] [--dh_heater DH_HEATER]
                           component tstart hours T_init pitch ccd_count
   
   Simulate an ECS run.
   
   positional arguments:
     component             The component to model: dpa, dea, or psmc.
     tstart                The start time of the ECS run in YYYY:DOY:HH:MM:SS format
     hours                 The length of the ECS run in hours.
     T_init                The initial temperature of the component in degrees C.
     pitch                 The pitch in degrees.
     ccd_count             The number of CCDs to clock.
   
   optional arguments:
     -h, --help            show this help message and exit
     --vehicle_load VEHICLE_LOAD
                           The vehicle load which is running. Default: None, meaning no vehicle load. If this parameter is set, the
                           input values of pitch and off-nominal roll will be ignored and the values from the vehicle load will be used.
     --off_nom_roll OFF_NOM_ROLL
                           The off-nominal roll. Default: 0.0
     --dh_heater DH_HEATER
                           Is the DH heater on (1) or off (0)? Default: 0/off.
Example 1
+++++++++

To run the 1DPAMZT model with the following conditions:

* Start time: 2015:100:12:45:30
* Length of ECS run: 24 hours
* Initial temperature: 10.0 degrees C
* Pitch: 150 degrees
* CCD count: 6
* Off-nominal roll: 12.0 degrees

.. code-block:: bash

    [~]$ simulate_ecs_run dpa 2015:100:12:45:30 24 10.0 150. 6 --off_nom_roll 12.0

Returns:

.. code-block:: text

    acispy: [INFO     ] 2021-09-07 13:47:29,088 Using model for dpa from chandra_models version = 3.35.2
    acispy: [INFO     ] 2021-09-07 13:47:29,423 Run Parameters
    acispy: [INFO     ] 2021-09-07 13:47:29,423 --------------
    acispy: [INFO     ] 2021-09-07 13:47:29,423 Start Datestring: 2015:100:12:45:30.000
    acispy: [INFO     ] 2021-09-07 13:47:29,423 Length of state in hours: 24.0
    acispy: [INFO     ] 2021-09-07 13:47:29,423 Stop Datestring: 2015:102:04:55:48.000
    acispy: [INFO     ] 2021-09-07 13:47:29,423 Initial Temperature: 10.0 degrees C
    acispy: [INFO     ] 2021-09-07 13:47:29,423 CCD/FEP Count: 6
    acispy: [INFO     ] 2021-09-07 13:47:29,424 Pitch: 150.0
    acispy: [INFO     ] 2021-09-07 13:47:29,424 Off-nominal Roll: 12.0
    acispy: [INFO     ] 2021-09-07 13:47:29,424 Detector Housing Heater: OFF
    acispy: [INFO     ] 2021-09-07 13:47:29,424 Model Result
    acispy: [INFO     ] 2021-09-07 13:47:29,425 ------------
    acispy: [INFO     ] 2021-09-07 13:47:29,425 The limit of 37.5 degrees C will be reached at 2015:100:19:17:44.816, after 23.53481599998474 ksec.
    acispy: [INFO     ] 2021-09-07 13:47:29,426 The limit is reached before the end of the observation.
    acispy: [WARNING  ] 2021-09-07 13:47:29,426 This observation is NOT safe from a thermal perspective.
    acispy: [INFO     ] 2021-09-07 13:47:30,134 Image of the model run has been written to ecs_run_dpa_6chip_2015:100:12:45:30.png.

.. image:: _images/ecs_run.png

Example 2
+++++++++

To run the 1DEAMZT model with the following conditions:

* Start time: 2017:069:15:40:00
* Length of ECS run: 24 hours
* Initial temperature: 7.5 degrees C
* Pitch: 150 degrees
* CCD count: 4
* Off-nominal roll: 0.0 degrees

.. code-block:: bash

    [~]$ simulate_ecs_run dea 2017:069:15:40:00 24 7.5 150. 4 --off_nom_roll 0.0

Returns:

.. code-block:: text

    acispy: [INFO     ] 2021-09-07 13:48:01,352 Using model for dea from chandra_models version = 3.35.2
    acispy: [INFO     ] 2021-09-07 13:48:01,632 Run Parameters
    acispy: [INFO     ] 2021-09-07 13:48:01,633 --------------
    acispy: [INFO     ] 2021-09-07 13:48:01,633 Start Datestring: 2017:069:15:40:00.000
    acispy: [INFO     ] 2021-09-07 13:48:01,633 Length of state in hours: 24.0
    acispy: [INFO     ] 2021-09-07 13:48:01,633 Stop Datestring: 2017:071:07:50:18.000
    acispy: [INFO     ] 2021-09-07 13:48:01,633 Initial Temperature: 7.5 degrees C
    acispy: [INFO     ] 2021-09-07 13:48:01,633 CCD/FEP Count: 4
    acispy: [INFO     ] 2021-09-07 13:48:01,633 Pitch: 150.0
    acispy: [INFO     ] 2021-09-07 13:48:01,633 Off-nominal Roll: 0.0
    acispy: [INFO     ] 2021-09-07 13:48:01,633 Detector Housing Heater: OFF
    acispy: [INFO     ] 2021-09-07 13:48:01,634 Model Result
    acispy: [INFO     ] 2021-09-07 13:48:01,635 ------------
    acispy: [INFO     ] 2021-09-07 13:48:01,635 The limit of 36.5 degrees C is never reached. 
    acispy: [INFO     ] 2021-09-07 13:48:01,635 This observation is safe from a thermal perspective.
    acispy: [INFO     ] 2021-09-07 13:48:02,529 Image of the model run has been written to ecs_run_dea_4chip_2017:069:15:40:00.png.

.. image:: _images/ecs_run2.png

Example 3
+++++++++

This example assumes that the vehicle loads are still running, which means
that the input values of the pitch and the off-nominal roll are ignored in 
favor of 

To run the 1DPAMZT model with the following conditions:

* Start time: 2017:256:03:20:00 
* Length of ECS run: 24 hours
* Initial temperature: 10.0 degrees C
* Pitch: 0 degrees (the value doesn't matter)
* CCD count: 6
* Vehicle load: SEP0917C

.. code-block:: bash

    [~]$ simulate_ecs_run dpa 2017:256:03:20:00 24 10.0 0.0 6 --vehicle_load SEP0917C

Returns:

.. code-block:: text

    acispy: [INFO     ] 2021-09-07 13:50:44,322 Modeling a 6-chip state concurrent with the SEP0917C vehicle loads.
    acispy: [INFO     ] 2021-09-07 13:50:46,713 Using model for dpa from chandra_models version = 3.35.2
    acispy: [INFO     ] 2021-09-07 13:50:46,958 Run Parameters
    acispy: [INFO     ] 2021-09-07 13:50:46,959 --------------
    acispy: [INFO     ] 2021-09-07 13:50:46,959 Start Datestring: 2017:256:03:20:00.000
    acispy: [INFO     ] 2021-09-07 13:50:46,959 Length of state in hours: 24.0
    acispy: [INFO     ] 2021-09-07 13:50:46,959 Stop Datestring: 2017:257:19:30:18.000
    acispy: [INFO     ] 2021-09-07 13:50:46,959 Initial Temperature: 10.0 degrees C
    acispy: [INFO     ] 2021-09-07 13:50:46,959 CCD/FEP Count: 6
    acispy: [INFO     ] 2021-09-07 13:50:46,959 Detector Housing Heater: OFF
    acispy: [INFO     ] 2021-09-07 13:50:46,960 Model Result
    acispy: [INFO     ] 2021-09-07 13:50:46,960 ------------
    acispy: [INFO     ] 2021-09-07 13:50:46,961 The limit of 37.5 degrees C will be reached at 2017:256:11:34:14.816, after 29.65481599998474 ksec.
    acispy: [INFO     ] 2021-09-07 13:50:46,961 The limit is reached before the end of the observation.
    acispy: [WARNING  ] 2021-09-07 13:50:46,961 This observation is NOT safe from a thermal perspective.
    acispy: [INFO     ] 2021-09-07 13:50:47,707 Image of the model run has been written to ecs_run_dpa_6chip_2017:256:03:20:00.png.

.. image:: _images/ecs_run3.png

``phase_scatter_plot``
----------------------

.. code-block:: text

    usage: phase_scatter_plot [-h] [--c_field C_FIELD] [--cmap CMAP] [--maude]
                              tstart tstop x_field y_field
    
    Make a phase scatter plot of one MSID or state versus another within a certain
    time frame.
    
    positional arguments:
      tstart             The start time in YYYY:DOY:HH:MM:SS format
      tstop              The stop time in YYYY:DOY:HH:MM:SS format
      x_field            The MSID or state to plot on the x-axis
      y_field            The MSID or state to plot on the y-axis
    
    optional arguments:
      -h, --help         show this help message and exit
      --c_field C_FIELD  The MSID or state to plot using colors
      --cmap CMAP        The colormap to use if plotting colors
      --maude            Use MAUDE to get telemetry data.

Example 1
+++++++++

.. code-block:: bash

    [~]$ phase_scatter_plot 2017:100 2017:200 1deamzt 1dpamzt

Returns:

.. image:: _images/phase_scatter_plot1.png

Example 2
+++++++++

.. code-block:: bash

    [~]$ phase_scatter_plot 2017:100 2017:200 1deamzt 1dpamzt --c_field ccd_count --cmap=jet

Returns:

.. image:: _images/phase_scatter_plot2.png

``phase_histogram_plot``
------------------------

.. code-block:: text

    usage: phase_histogram_plot [-h] [--scale SCALE] [--cmap CMAP] [--maude]
                                tstart tstop x_field y_field x_bins y_bins
    
    Make a phase plot of one MSID or state versus another within a certain time
    frame.
    
    positional arguments:
      tstart         The start time in YYYY:DOY:HH:MM:SS format
      tstop          The stop time in YYYY:DOY:HH:MM:SS format
      x_field        The MSID or state to plot on the x-axis
      y_field        The MSID or state to plot on the y-axis
      x_bins         The number of bins on the x-axis
      y_bins         The number of bins on the y-axis
    
    optional arguments:
      -h, --help     show this help message and exit
      --scale SCALE  Use linear or log scaling for the histogram, default 'linear'
      --cmap CMAP    The colormap for the histogram, default 'hot'
      --maude        Use MAUDE to get telemetry data.

Example
+++++++

.. code-block:: bash

    [~]$ phase_histogram_plot 2017:100 2017:200 1deamzt 1dpamzt 40 40 --scale=log --cmap=hsv

Returns:

.. image:: _images/phase_histogram_plot.png
