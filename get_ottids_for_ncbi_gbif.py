import requests
import json
import sys


def get_from_gbif_id(name):
    url = 'https://api.opentreeoflife.org/v3/taxonomy/taxon_info'
    payload = json.loads('{"source_id":"gbif:'+name+'"}')
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    
    id = None
    if 'ott_id' in r.json():
        id = r.json()['ott_id']
    return id

def get_from_ncbi_id(name):
    url = 'https://api.opentreeoflife.org/v3/taxonomy/taxon_info'
    payload = json.loads('{"source_id":"ncbi:'+name+'"}')
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    id = None
    if 'ott_id' in r.json():
        id = r.json()['ott_id']
    return id

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python "+sys.argv[0]+" ncbi|gbif filename"
        sys.exit(0)
    
    ncbi = True
    if sys.argv[1] == "gbif":
        ncbi = False

    of = open(sys.argv[2]+".nomatch.txt","w")
    fn = open(sys.argv[2],"r")
    for i in fn:
        i = i.strip()
        nm = i
        id = None
        if ncbi == True:
            id = get_from_ncbi_id(nm)
        else:
            id = get_from_gbif_id(nm)
        if id != None:
            print nm,id
        else:
            of.write(nm+"\n")
    fn.close()
    of.close()
