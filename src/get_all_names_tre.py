import tree_reader
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "python "+sys.argv[0]+" tre"
        sys.exit(0)
    tre = tree_reader.read_tree_file(sys.argv[1])[0]
    for i in tre.iternodes():
        if len(i.label) > 0:
            if "mrca" not in i.label:
                print i.label
