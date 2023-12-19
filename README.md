# AC6 Optimiser
(Not updated to 1.05 yet)

If you just want the download, it's the .exe in the build folder. If you want to make sure this doesn't install a bitcoin miner, look at the source code and build it yourself (I just use pyinstaller).

Mostly feature complete if a bit slow if few restrictions are placed on it. Planning to add:
- I am aware of formulas for all sorts of speed (boost, AB, QB, Tetra Hover, Tank travel etc), but need to implement them
- Some function that searches in a weight bracket around the current weight to see if slight increases/decreases in weight or speed would lead to a big EHP boost/loss
- Some of the displayed stats are not rounded bc I couldn't be bothered
- Ultimately, I want this to be a web app so people don't have to download strange .exes. I'd have to learn Flask (probably?) and HTML for that though, so it'll take time

If you have additional feature suggestions/find issues or bugs, please let me know.