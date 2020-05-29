#! /usr/bin/env nix-shell
#! nix-shell -i bash -p python3Packages.notebook python3Packages.matplotlib python3Packages.scikitlearn

jupyter-notebook --no-browser
