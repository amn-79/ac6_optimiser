# AC6 Optimiser
Update version: Patch 1.07.1, App Ver 70

With thanks to u/Quimperinos, whose AC6 Virtual Garage spreadsheet gave me the speed formulae, and u/TraumaHunter, who created the spreadsheet that my data is based on

# Updates
## 16/11/2024
- Updated data files to new patch
- Added speed optimisation
- Changed UI to show more information, new optimisation options
  - Added lock-on time for hard lock (soft lock is one third of hard lock time, roughly)
  - Added recharge delay for normal and redline recharge
  - Added system recovery
  - Added speed statistics for a bunch of movement types
- Deprecated firearm spec and free EN minimum for better options (actual target tracking, actual EN recharge speed)
- Renamed area search to interval search

## 20/09/2024
- Changed data files due to new patch
- Added app spec to repository to make building it yourself easier

## 09/02/2024
- Changed data files due to new patch

## 29/12/2023
- Added interval search mode

# Notes
Build uses pyinstaller. Simply run "pyinstaller app.spec", or alternatively download the prebuilt .exe in the dist folder.

Mostly feature complete if a bit slow if few restrictions are placed on it. 

I'm probably not developing this further since my interest has waned. Possible extensions would be:
- I am aware of formulas for all sorts of speed (boost, AB, QB, Tetra Hover, Tank travel etc), but need to implement them
- Ultimately, I would like this to be a web app so people don't have to download strange .exes. I'd have to learn Flask (probably?) and HTML for that though, so it'll take time

If you have additional feature suggestions/find issues or bugs, please let me know.

## Interval search
The purpose of this is to check how much more "juice" you could get out of relaxing restrictions by a bit.
Currently only works for explicit weight restrictions, and checks in intervals of 1000 around the selected value.

Please note that this likely doesn't show the full picture! If your steps are e.g. 48000 and 49000, then the graph will show the "progression" as being smooth - but this is not actually the case. For one, the weight -> EHP/AP/whatever relationship will always be a step-function as new combinations become possible with weaker restrictions, and additionally it is absolutely possible that there is some combination at 48500 that you are skipping because it is lower in the target stat than what is possible at 49000.

Planned to be usable for more restrictions in the future, with custom step size.
If no solution is possible for some reason (maximum weight set too low, probably), the graph gets sent a 0 instead which sort of messes up the scaling of the graphic.

## Speed and options
This optimizer is pretty computationally intensive when optimising for average EHP (which is the average of AP / damage reduction for all damage types; for coral, this term is just AP), which sadly is also the most interesting stat.
This shows especially when using area search. 

Adding more restrictions (like selecting a specific leg type) or forcing selection of single parts will speed up calculations since you reduce the number of possible combinations. Alternatively, simple stats like raw AP or attitude stability (AS) are also faster.