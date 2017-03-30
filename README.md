# OpenTree PY Toys


## Pruning OpenTree synth tree
If you are trying to calculate things on a subset of the OpenTree synth tree, here are some steps to get that done. These require some of the [phyx](https://github.com/FePhyFoFum/phyx) tools and python scripts that are presented here but that should be it.

    - get the latest synth tree from [here](https://tree.opentreeoflife.org/about/synthesis-release)

    - get OTT ids for your taxa using either
        - the scripts in this repo `python get_ottids_for_taxa.py file.ids > file.ids.ottids`
        - the [peyotl](https://opentreeoflife.github.io/peyotl/installation/) set of tools 
        - the OpenTree [APIs](https://github.com/OpenTreeOfLife/germinator/wiki/Open-Tree-of-Life-Web-APIs)

    - to make the scripts run better, I recommend pruning it down to just what you use (so, plants for example)
        - `pxmrcacut -m cut_mrca_plants -t opentree9.1_tree/labelled_supertree/labelled_supertree.tre > vas_opentree_9.1.tre`
        - there are included `cut_mrca` files for different groups in this repo
        - `pxmrcacut` is a program in the `phyx` package
            
    - get the list of taxa 
        - `python trace_tree.py vas_opentree_9.1.tre file.ids.ottids  > vas_nms.tre`
        - if there is enough interest, I will make this a java program for speed and portability
