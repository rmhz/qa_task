import json
import httplib

conn = httplib.HTTPConnection("qainterview.cogniance.com")
try:
    conn.connect()
except:
    raise Exception("Connection error")
    

###test1 - GET Method
#Reques a list of candidates, expect status 200
conn.request("GET", "/candidates")
r1 = conn.getresponse()
status = r1.status
init_cand_len = len(r1.read())
if status == 200:
    print 'GET /candidates method -> OK'
else:
    print 'GET /candidates method -> Fail'


###test2 - POST Method
#Add new valid candidate, expect status 201
body = json.dumps({'name': "name_test", 'position': "pos_test"})
header = {'Content-Type': 'application/json'}
conn.request("POST", "/candidates", body, header)
r2 = conn.getresponse()
status = r2.status
r2.read()
if status == 201:
    print 'POST new candidate method -> OK'
else:
    print 'POST new candidate method -> Fail'

###test2_1
#Add new invalid candidate - name absent, expect status 400
body = json.dumps({'position': "pos_test"})
header = {'Content-Type': 'application/json'}
conn.request("POST", "/candidates", body, header)
r21 = conn.getresponse()
status = r21.status
r21.read()
if status == 400:
    print 'POST new candidate without name method -> OK'
else:
    print 'POST new candidate without name method -> Fail'

###test2_2
#Add new invalid candidate - content-type absent, expect status 400
body = json.dumps({'name': "name_test", 'position': "pos_test"})
header = {}
conn.request("POST", "/candidates", body, header)
r22 = conn.getresponse()
status = r22.status
r22.read()
if status == 400:
    print 'POST new candidate without header method -> OK'
else:
    print 'POST new candidate without header method -> Fail'


###test3
#Request list of candidates after addition of new candidate
#Expect length of data increased -> some data added to server
#Getting an id of last added candidate
conn.request("GET", "/candidates")
r3 = conn.getresponse()
resp_data = r3.read()
new_cand_len = len(resp_data)
candidates = json.loads(resp_data)['candidates']
cand_id=candidates[-1:][0]['id']
if new_cand_len > init_cand_len:
    print 'Some data added to server -> OK'
else:
    print 'Some data added to server -> Fail'

###test4
#Request candidate data by <cand_id>, expect status 200
conn.request("GET", "/candidates/"+str(cand_id))
r4 = conn.getresponse()
status = r4.status
r4.read()
if status == 200:
    print 'GET /candidates/<cand_id> method -> OK'
else:
    print 'GET /candidates/<cand_id> method -> Fail'

###test5
#Delete a candidate with <cand_id>, expect status 200
conn.request("DELETE", "/candidates/"+str(cand_id))
r5 = conn.getresponse()
status = r5.status
r5.read()
if status == 200:
    print 'DELETE /candidates/<cand_id> method -> OK'
else:
    print 'DELETE /candidates/<cand_id> method -> Fail'

conn.close()
