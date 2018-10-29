import tree_reader
import tree_utils
import sys
import node as node

"""
here we want to add taxa where you give the mrca
so in names.txt you would say
mrcatomove1,mrca2tomove mrca1taxa,mrca2taxa
"""

# this will either be sister or will be at a polytomy
add_as_sister = True

def fix_height(startnode,targetheight):
    if len(startnode.children) == 0:
        startnode.length = float(targetheight+startnode.length)
    else:
        for i in startnode.leaves():
            route = []
            tnode = i
            while tnode != startnode:
                route.append(tnode)
                tnode = tnode.parent
            for j in route:
                j.length = float(targetheight)/len(route)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "python "+sys.argv[0]+" tree names1(,sep) names2(,sep)"
        sys.exit(0)
    
    tree = tree_reader.read_tree_file_iter(sys.argv[1]).next()
    tree_utils.set_heights(tree)

    nms1 = sys.argv[2].split(",")
    nms2 = sys.argv[3].split(",")

    replace = {}#key is single mrca taxon, value is node that is to be used
    print >> sys.stderr, nms1
    print >> sys.stderr, nms2
    mrca1 = tree_utils.get_mrca_wnms(nms1,tree)
    mrca2 = tree_utils.get_mrca_wnms(nms2,tree)
    print >> sys.stderr, mrca1.get_newick_repr()
    print >> sys.stderr, mrca2.get_newick_repr()
    # will be a polytomy
    if add_as_sister == False:
        x = mrca2.parent
    # will be sister
    else:
        s = mrca2
        p = s.parent
        nn = node.Node()
        nn.length = s.length/2.
        s.length = nn.length
        p.remove_child(s)
        p.add_child(nn)
        nn.add_child(s)
        x = nn
    p = mrca1.parent
    if len(p.children) == 2 and x != p:
        pp = p.parent
        c = None
        for j in p.children:
            if j != mrca1:
                c = j
        pp.add_child(c)
        pp.remove_child(p)
        c.parent = pp
        c.length = c.length + p.length
    else:
        p.remove_child(mrca1)
    tree_utils.set_heights(x)
    try:
        x.add_child(mrca1)
        if add_as_sister == True:
            fix_height(x,x.height)
        else:
            fix_height(mrca1,x.height-mrca1.length)
        print >> sys.stderr, x.height,mrca1.length
    except:
        print >>sys.stderr, "problem adding child",mrca1.get_newick_repr(),"to",x.get_newick_repr()
    print >> sys.stderr,x.get_newick_repr(True)
    print >> sys.stderr,x.parent.get_newick_repr(True)

    print tree.get_newick_repr(True)+";"
