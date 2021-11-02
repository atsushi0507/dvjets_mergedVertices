# Merged vertices study for SUSY DV studies

This repo contains python-based scripts for merged vertices estimation.

## Instructions for running the script
### Data driven-method
The script to calculate the significance and merged vertices mass:
```
python sigCalc.py --sr [HighPtSR or TracklessSR] -tag [a,d, or e]
```
The output root file is created in outputFiles. The directory is created automatically.

The output is ntuple, and it may better to store histograms, too. This is a remnant of my developing steps.


Plotting significance and mass of the merged vertices (in plottingScript):
```
python plotSignificanceAndMass.py -sr [HighPtSR or TracklessSR] -tag [a, d, or e]
```
This script extract the significance and merged mass both for same and mixed event from the output of the `sigCalc.py`.


### Truth method
The script to choose merged vertices DV from dijet MC:
```
python makeMVTreeMC.py -sr [HighPtSR or TracklessSR] --tag [a, d, or e]
```
This script is developed based on hadronic interaction study.

Plotting the merged vertices mass, and so on (in plottingScript).
```
python plotMass.py -tag [a, d, or e] --sr [HighPtSR or TracklessSR] (-doHI -tc)
```
Find merged vertices using truth information.
Use doHI flag to reject the hadronic interaction from the merged vertices. If the track parent PDGID is correspond to proton or pion, the vertex is rejected.

Use tc flag to load the track cleaning file.