import requests
import json
import sys


def get_tree(inurl,ids):
    url = inurl+'/induced_subtree'
    idss = "{\"ott_ids\":["+",".join(ids)+"]}"
    payload = json.loads(idss)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    
    ne = None
    unmatched = None
    if 'newick' in r.json():
        ne = r.json()['newick']
        unmatched = r.json()['unmatched_ott_ids']
    
    return ne,unmatched

def rename_tree(inurl,ts):
    url = inurl+'/rename_tree'
    idss = "{\"newick\":\""+ts+"\"}"
    payload = json.loads(idss)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    
    ne = None
    unmatched = None
    if 'newick' in r.json():
        ne = r.json()['newick']
        unmatched = r.json()['unmatched_ott_ids']
    
    return ne,unmatched

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python "+sys.argv[0]+" url filename"
        sys.exit(0)
    
    url = sys.argv[1]
    of = open(sys.argv[2]+".nomatch.txt","w")
    fn = open(sys.argv[2],"r")
    nms = []
    for i in fn:
        i = i.strip()
        nm = i
        if "ott" in nm:
            nm = nm.replace("ott","")
        nms.append(nm)
    fn.close()
    of.close()
    ne,unmatached = get_tree(url,nms)
    ne,unmatached = rename_tree(url,ne)
    print ne