import requests
import json
import sys


def get_name_id(name):
    url = 'https://api.opentreeoflife.org/v3/taxonomy/taxon_info'
    payload = json.loads('{"ott_id":'+name+'}')
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    
    id = None
    if 'tax_sources' in r.json():
        id = r.json()['unique_name']
    return id

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "python "+sys.argv[0]+" filename"
        sys.exit(0)
    

    of = open(sys.argv[1]+".nomatch.txt","w")
    fn = open(sys.argv[1],"r")
    for i in fn:
        i = i.strip()
        nm = i
        if "ott" in nm:
            nm = nm.replace("ott","")
        id = get_name_id(nm)
        if id != None:
            print nm+"\t"+id
        else:
            of.write(nm+"\n")
    fn.close()
    of.close()
