# AC6 Optimiser
Update version: Patch 1.06.1, App Ver 60

If you just want the download, it's the .exe in the build folder. If you want to make sure this doesn't install a bitcoin miner, look at the source code and build it yourself (I just use pyinstaller).

Mostly feature complete if a bit slow if few restrictions are placed on it. 

I'm probably not developing this further since my interest has waned. Possible extensions would be:
- I am aware of formulas for all sorts of speed (boost, AB, QB, Tetra Hover, Tank travel etc), but need to implement them
- Ultimately, I would like this to be a web app so people don't have to download strange .exes. I'd have to learn Flask (probably?) and HTML for that though, so it'll take time

If you have additional feature suggestions/find issues or bugs, please let me know.

## Added area search
The purpose of this is to check how much more "juice" you could get out of relaxing restrictions by a bit.
Currently only works for explicit weight restrictions, and checks in intervals of 1000 around the selected value.

Please note that this likely doesn't show the full picture! If your steps are e.g. 48000 and 49000, then the graph will show the "progression" as being smooth - but this is not actually the case. For one, the weight -> EHP/AP/whatever relationship will always be a step-function as new combinations become possible with weaker restrictions, and additionally it is absolutely possible that there is some combination at 48500 that you are skipping because it is lower in the target stat than what is possible at 49000.

Planned to be usable for more restrictions in the future, with custom step size.
If no solution is possible for some reason (maximum weight set too low, probably), the graph gets sent a 0 instead which sort of messes up the scaling.

## Speed and options
This optimizer is pretty computationally intensive when optimising for average EHP (which is the average of AP / damage reduction for all damage types; for coral, this term is just AP), which sadly is also the most interesting stat.
This shows especially when using area search. 

Adding more restrictions (like selecting a specific leg type) or forcing selection of single parts will speed up calculations since you reduce the number of possible combinations. Alternatively, simple stats like raw AP or attitude stability (AS) are also faster.