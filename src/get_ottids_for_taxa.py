import requests
import json
import sys

def get_id_hyphen(name):
    url = 'https://api.opentreeoflife.org/v3/tnrs/autocomplete_name'
    nm = name.split("-")[0]
    print nm
    payload = json.loads('{"name":"'+nm+'"}')
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    id = r.json()[0]['ott_id']
    return id

def get_id(name):
    url = 'https://api.opentreeoflife.org/v3/tnrs/match_names'
    payload = json.loads('{"names":["'+name+'"]}')
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    id = None
    for i in r.json()['results']:
        id = i['matches'][0]['taxon']['ott_id']
        break
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
        if "_" in nm:
            nm = " ".join(i.split(" ")[0].split("_"))
        id = None
        if "-" in nm:
            id = get_id_hyphen(nm)
        else:
            id = get_id(nm)
        if id != None:
            print nm+"\t"+str(id)
        else:
            of.write(nm+"\n")
    fn.close()
    of.close()
