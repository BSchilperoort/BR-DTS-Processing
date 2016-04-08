# BR-DTS-Processing
Python scripts to process the raw DTS data and calculate the bowen ratio or fluxes
The scripts work for Python 3. The required non-standard libraries are _numpy_ and _matplotlib_. [Pyzo](http://www.pyzo.org/) is a programming enviroment for Python 3, and contains all required libraries along with many more scientific computing libraries. You can download it [**here**](http://www.pyzo.org/downloads.html).

##### Raw ultima data
The Ultima xml files can be converted to an ascii file containing all the temperature data using the 'xml_to_txt.py' file. The folder xml_conversion contains example data.

##### Temperature processing and plotting
Functions for importing the processed data can be found in the data_processing folder (dataImports). It also contains some custom functions which are used (customFunctions).

An example of how to read out, process and plot the Ultima data is located under data_processing/dts_plot_example.py
