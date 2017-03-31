import tree_reader
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python "+sys.argv[0]+" tre ottids_name"
        sys.exit(0)

    tre = tree_reader.read_tree_file(sys.argv[1])[0]
    names = {}
    nf = open(sys.argv[2],"r")
    for i in nf:
        spls = i.strip().split("\t")
        names["ott"+spls[0]] = spls[1]
    nf.close()
    
    for i in tre.iternodes():
        if i.label in names:
            i.label = names[i.label].replace(" ","_")
        else:
            i.label = ""

    going = True
    while going:
        found = False
        for i in tre.iternodes():
            if i.parent != None and len(i.children) == 1 and i.label == "":
                par = i.parent
                ch = i.children[0]
                par.remove_child(i)
                par.add_child(ch)
                found = True
                break
        if found == False:
            going = False
            break

    print tre.get_newick_repr(False)+";"
