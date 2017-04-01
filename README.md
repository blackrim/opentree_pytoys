# OpenTree PY Toys


## Pruning OpenTree synth tree
If you are trying to calculate things on a subset of the OpenTree synth tree, here are some steps to get that done. These require some of the [phyx](https://github.com/FePhyFoFum/phyx) tools and python scripts that are presented here but that should be it. The `get_ottids_for_taxa.py` script needs the `request` python module that can be found [here](http://docs.python-requests.org/en/master/).

- get the latest synth tree from [here](https://tree.opentreeoflife.org/about/synthesis-release)

- get OTT ids for your taxa using either
  - the scripts in this repo `python get_ottids_for_taxa.py file.ids > file.ids.ottids`. The `file.ids` file should have a `Genus species` on each line.
  - the [peyotl](https://opentreeoflife.github.io/peyotl/installation/) set of tools 
  - the OpenTree [APIs](https://github.com/OpenTreeOfLife/germinator/wiki/Open-Tree-of-Life-Web-APIs)

- if you aren't using `pxtrt` (from [phyx](https://github.com/FePhyFoFum/phyx))to trace your tree, I recommend pruning it down to just what you use (so, plants for example). You don't have to do this if you use the `phyx` program `pxtrt` to trace the tree because it can read larger trees.
  - `pxmrcacut -m cut_mrca_plants -t opentree9.1_tree/labelled_supertree/labelled_supertree.tre > vas_opentree_9.1.tre`
  - there are included `cut_mrca` files for different groups in this resources dir in the repo repo
  - `pxmrcacut` is a program in the `phyx` package
            
- get the list of taxa as a tree
  - using python - `python trace_tree.py vas_opentree_9.1.tre file.ids.ottids  > vas_nms.tre`
  - or you can use `pxtrt` from `phyx`. You will need to isolate the ids from `file.ids.ottids`. You can do this with `awk -F '\t' '{print "ott"$2}' file.ids.ottids > file.justids.ottids`. Then you can run `pxtrt` like `pxtrt -t opentree9.1_tree/labelled_supertree/labelled_supertree.tre -f file.justids.ottids > traced.tre`. 

## An example with _Fire_Border_Hot_Sauce_ from _TacoBell_
In the examples folder, there is a TACO_BELL directory. There is a file called `border_hot_sauce` with the scientific names of the ingredients. Here are the steps to a readable tree:

- `python ../../src/get_ottids_for_taxa.py border_hot_sauce > names_ottids`
- `awk -F '\t' '{print "ott"$2}' names_ottids > justids.ottids`
- I have already downloaded the most recent synth (see above) into a directory called `opentree9.1_tree`. So I run `pxtrt opentree9.1_tree/labelled_supertree/labelled_supertree.tre -f justids.ottids > out.tre`
- `out.tre` is the tree that you want but the ids are ottids, so not really readable. To convert, we do three simple steps:
  - `python get_all_names_tre.py out.tre > alltreenames`
  - `python get_name_for_ottids.py alltreenames > allnames.ottids_names`
  - `python convert_ottids_names_tre.py out.tre allnames.ottids_names > final.tre`

A lot of steps right now but I will simplify soon! Right now, going for flexibility.
