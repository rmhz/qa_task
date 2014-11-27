import json
import httplib

conn = httplib.HTTPConnection("qainterview.cogniance.com")

###test1 - GET Method
conn.request("GET", "/candidates")
r1 = conn.getresponse()
status = r1.status
init_cand_len = len(r1.read())
if status == 200:
    print 'GET /candidates method -> OK'
else:
    print 'GET /candidates method -> Fail'


###test2 - POST Method
body = json.dumps({'name': "name_test", 'position': "pos_test"})
header = {'Content-Type': 'application/json'}
conn.request("POST", "/candidates", body, header)
r2 = conn.getresponse()
status = r2.status
print 

###test3
conn.request("GET", "/candidates")
r3 = conn.getresponse()
candidates = json.loads(r3.read())['candidates']
cand_id=candidates[-1:][0]['id']
print r3.status, len(r3.read()), cand_id

###test4
conn.request("GET", "/candidates/"+str(cand_id))
r4 = conn.getresponse()
print r4.status, r4.read()

###test5
conn.request("DELETE", "/candidates/"+str(cand_id))
r5 = conn.getresponse()
print r5.status

conn.close()
