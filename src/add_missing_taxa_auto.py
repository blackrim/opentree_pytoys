import tree_reader
import tree_utils
import sys
import cnode as node


"""
this will add taxa to a tree based on the MRCA of the common parts of the name

typically that will be the first part so like

you want to add
a_b

and it will find all the mrca of a_c,a_d and so on and add a_b to that mrca
"""

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python "+sys.argv[0]+" infile.tre names.txt"
        sys.exit(0)
    

    tree = tree_reader.read_tree_file_iter(sys.argv[1]).next()
    tree_utils.set_heights(tree)
    mrca_checks = {}

    for i in tree.leaves():
        spls = i.label.split("_")
        try:
            mrca_checks[spls[0]].append(i)
        except:
            mrca_checks[spls[0]] = []
            mrca_checks[spls[0]].append(i)

    of = open(sys.argv[2],"r")
    for i in of:
        nm = i.strip()
        nm1 = nm.split("_")[0]
        if nm1 in mrca_checks:
            print nm1,mrca_checks[nm1]
            x = None
            if len(mrca_checks[nm1]) == 1:
                x = mrca_checks[nm1][0]
            else:
                x = tree_utils.get_mrca(mrca_checks[nm1],tree)
            print x.get_newick_repr()
            n2 = node.Node()
            n2.label = nm
            # is a tip
            if len(x.children) == 0:
                p = x.parent
                # add a child
                n = node.Node()
                n.length = x.length/2.
                x.length = n.length
                p.remove_child(x)
                n.add_child(x)
                n2.length = x.length
                n.add_child(n2)
                p.add_child(n)
                tree_utils.set_heights(n)
            else:
                n2.length = x.height
                x.add_child(n2)
            mrca_checks[nm1].append(n2)
            print >> sys.stderr, "adding",nm,"to",nm1
        else:
            print >> sys.stderr, nm1,"not in tree"
    of.close()

    print tree.get_newick_repr(True)