import sys
import os
import tree_reader
import tree_utils

"""
assuming that the datedtre just has ott ids as the tip names

assuming the labelled_supertree has ott in front of the ott ids
"""

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python "+sys.argv[0]+" datedtree labelled_superrtree"
        sys.exit(0)
    dated = tree_reader.read_tree_file_iter(sys.argv[1]).next()
    ott = tree_reader.read_tree_file_iter(sys.argv[2]).next()
    tree_utils.set_heights(dated)
    ottlvsd = {} #key is name and value is node
    for i in ott.iternodes():
        ottlvsd[i.label] = i
    
    for i in dated.leaves():
        try:
            i.data["node"] = ottlvsd["ott"+i.label]
        except:
            print >>sys.stderr,"not matched",i.label
            continue
    
    done = set()
    dates = {} # key is node, value is date
    dates_names = {} #key is node, value is mrca string
    for i in dated.iternodes(order="preorder"):
        if len(i.children) == 0:
            continue
        else:
            nds = [] 
            for j in i.leaves():
                if "node" in j.data:
                    nds.append(j.data["node"])
            if len(nds) > 1:
                x = tree_utils.get_mrca(nds,ott)
                if x in done:
                    continue
                done.add(x)
                dates[x] = i.height
                dates_names[x] = x.children[0].leaves()[0].label+","+x.children[1].leaves()[0].label
    
    # check backwards
    dele = set()
    for i in dates:
        if i in dele:
            continue
        cur = i
        while cur != None:
            try:
                if dates[cur] < dates[i]:
                    dele.add(cur)
            except:
                1 + 1
            cur = cur.parent

    for i in dele:
        del dates[i]

    for i in ott.iternodes(order="preorder"):
        if i in dates:
            print dates_names[i],dates[i]