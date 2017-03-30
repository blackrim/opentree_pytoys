import requests
import json
import sys


def get_gbif_id(name):
    url = 'https://api.opentreeoflife.org/v3/taxonomy/taxon_info'
    payload = json.loads('{"ott_id":'+name+'}')
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    
    id = None
    if 'tax_sources' in r.json():
        for i in r.json()['tax_sources']:
            if "gbif" in i:
                id = i.split(":")[1]
    return id

def get_ncbi_id(name):
    url = 'https://api.opentreeoflife.org/v3/taxonomy/taxon_info'
    payload = json.loads('{"ott_id":'+name+'}')
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    id = None
    if 'tax_sources' in r.json():
        for i in r.json()['tax_sources']:
            if "ncbi" in i:
                id = i.split(":")[1]
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
            id = get_ncbi_id(nm)
        else:
            id = get_gbif_id(nm)
        if id != None:
            print nm,id
        else:
            of.write(nm+"\n")
    fn.close()
    of.close()
