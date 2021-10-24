# PythonScripts
Collection of miscellaneous Python scripts

This also includes a runScript to execute a jupyter for easy coding of python

## Use without nix
```
python3 -m venv env
source env/bin/activate
```

## pdf-utilities
For now allows easy splitting of pdf into its chapters

## stacked Bars
This script has the goal to draw data into a graph of stacked data. This is for example useful if you want to show a execution time is distributed over parts of a program and compare this distribution between different implementations of the algorithm. As this is about execution time error bars are included to indicate standard deviation.

## Youtube RSS Converter
```
python youtube_rss_converter.py INPUT COOKIE
```
Convert a given `INPUT` file with a list of youtube account URLs into a list of RSS feed urls. Note the COOKIE parameter needs to be the CONSENT Cookie from youtube else the script won't work as youtube returns a cookie consent page for each request. An example call may look like this:

```
python youtube_rss_converter.py input "CONSENT=YES+fjeidndsop392-3014902klnvk3"
```

## Filter
Filter a given input for the word tuples given in the filter. Each line of the filter is split into words and the program will output all lines of the input that match all the words of at least one line of the filter line. This is especially useful if you have a list of names and a list of names with more information and you want to filter all names with there information that are on the first list.

## Train Passwords
I created this script to get used to typing a new password. It allows for entering a password and then to type it repeatingly getting a correct/wrong feedback, hopefully without committing the password to the terminal output nor disk.
