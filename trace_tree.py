import tree_reader
import sys



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python "+sys.argv[0]+" treefile namesfile"
        sys.exit(0)
    treefile = open(sys.argv[1],"r")
    tfl = tree_reader.read_tree_string(treefile.readline())
    lvsd = {}
    for i in tfl.leaves():
        lvsd[i.label] = i
    treefile.close()

    namesfile = open(sys.argv[2],"r")
    names = []
    namesd = {}
    for i in namesfile:
        nm = "ott"+i.strip().split(" ")[-1]
        names.append(nm)
        namesd[nm] = "_".join(i.strip().split(" ")[0:-1])
    namesfile.close()

    for i in names:
        if i in lvsd:
            lvsd[i].data["paint"] = True
            cur = lvsd[i]
            while cur != tfl:
                cur = cur.parent
                if "paint" in cur.data:
                    break
                else:
                    cur.data["paint"] = True
            lvsd[i].label = namesd[i]
        
    print tfl.get_newick_repr_paint()+";"
