# OpenTree PY Toys


## Pruning OpenTree synth tree
If you are trying to calculate things on a subset of the OpenTree synth tree, here are some steps to get that done. These require some of the [phyx](https://github.com/FePhyFoFum/phyx) tools and python scripts that are presented here but that should be it. The `get_ottids_for_taxa.py` script needs the `request` python module that can be found [here](http://docs.python-requests.org/en/master/).

- get the latest synth tree from [here](https://tree.opentreeoflife.org/about/synthesis-release)

- get OTT ids for your taxa using either
  - the scripts in this repo `python get_ottids_for_taxa.py file.ids > file.ids.ottids`. The `file.ids` file should have a `Genus species` on each line.
  - the [peyotl](https://opentreeoflife.github.io/peyotl/installation/) set of tools 
  - the OpenTree [APIs](https://github.com/OpenTreeOfLife/germinator/wiki/Open-Tree-of-Life-Web-APIs)

- to make the scripts run better, I recommend pruning it down to just what you use (so, plants for example). You don't have to do this if you use the `phyx` program `pxtrt` to trace the tree because it can read larger trees.
  - `pxmrcacut -m cut_mrca_plants -t opentree9.1_tree/labelled_supertree/labelled_supertree.tre > vas_opentree_9.1.tre`
  - there are included `cut_mrca` files for different groups in this repo
  - `pxmrcacut` is a program in the `phyx` package
            
- get the list of taxa 
  - `python trace_tree.py vas_opentree_9.1.tre file.ids.ottids  > vas_nms.tre`
  - or you can use `pxtrt` from `phyx`. You will need to isolate the ids from `file.ids.ottids`. You can do this with `awk -F '\t' '{print "ott"$2}' file.ids.ottids > file.justids.ottids`. Then you can run `pxtrt` like `pxtrt -t opentree9.1_tree/labelled_supertree/labelled_supertree.tre -f file.justids.ottids > traced.tre`. 
