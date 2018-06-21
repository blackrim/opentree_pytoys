import tree_reader
import tree_utils
import sys
import node as node

"""
here we want to add taxa where you give the mrca
so in names.txt you would say
taxatoadd,mrca1taxa,mrca2taxa


need to sort them by the mrcas and then do them all at once
"""

# this will either be sister or will be at a polytomy
add_as_sister = False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python "+sys.argv[0]+" infile.tre names.txt"
        sys.exit(0)
    
    tree = tree_reader.read_tree_file_iter(sys.argv[1]).next()


    tree_utils.set_heights(tree)

    of = open(sys.argv[2],"r")
    replace = {}#key is single mrca taxon, value is node that is to be used
    for i in of:
        spls = i.strip().split(",")
        nms = spls[1:]
        nm = spls[0]
        x = None
        if len(nms) == 1:
            if nms[0] in replace:
                x = replace[nms[0]]
            else:
                for j in tree.leaves():
                    if j.label == nms[0]:
                        x = j
                        break
                p = x.parent
                nn = node.Node()
                nn.length = x.length/2.
                x.length = nn.length
                p.remove_child(x)
                p.add_child(nn)
                nn.add_child(x)
                x = nn
                replace[nms[0]] = x
                tree_utils.set_heights(x)
        else:
            # will be a polytomy
            if add_as_sister == False:
                x = tree_utils.get_mrca_wnms(nms,tree)
            # will be sister
            else:
                s = tree_utils.get_mrca_wnms(nms,tree)
                p = s.parent
                nn = node.Node()
                nn.length = s.length/2.
                s.length = nn.length
                p.remove_child(s)
                p.add_child(nn)
                nn.add_child(s)
                x = nn
                tree_utils.set_heights(x)
        print >> sys.stderr,x.get_newick_repr()
        n2 = node.Node()
        n2.label = nm
        n2.length = x.height
        x.add_child(n2)
        print >> sys.stderr, "adding",nm,"to",x
    of.close()

    print tree.get_newick_repr(True)+";"
