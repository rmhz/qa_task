import json, requests, random, pytest

def getCandidatesList(header={}, body=""):
    response = requests.get('http://qainterview.cogniance.com/candidates',
                            data = body,
                            headers = header)
    return {'status':response.status_code,
            'header':response.headers,
            'body':response.text}

def getCandidate(cand_id, header={}, body=""):
    response = requests.get('http://qainterview.cogniance.com/candidates/'+str(cand_id),
                            data = body,
                            headers = header)
    return {'status':response.status_code,
            'header':response.headers,
            'body':response.text}

def postCandidate(header, body):
    response = requests.post('http://qainterview.cogniance.com/candidates',
                             data = body,
                             headers = header)
    return {'status':response.status_code,
            'header':response.headers,
            'body':response.text}

def deleteCandidate(cand_id, header={}, body=""):
    response = requests.delete('http://qainterview.cogniance.com/candidates/'+str(cand_id),
                               data = body,
                               headers = header)
    return {'status':response.status_code,
            'header':response.headers,
            'body':response.text}    


##class TestQA():
##    def test_getCandidatesList(self):
##        assert (getCandidatesList()['status'] == 200)
##
##    def test_validCandidateAdd(self):
##        body = json.dumps({'name': 'name_test', 'position': "pos_test"})
##        header = {'Content-Type': 'application/json'}
##        response = postCandidate(header, body)
##        assert (response['status'] == 201)
##        return json.loads(response['body'])['candidate']['id']
##
##    def test_getCandidate(self):
##        cand_id = self.test_validCandidateAdd()
##        assert (getCandidate(cand_id)['status'] == 200)
##
##    def test_dataAddedToServer(self):
##        init_length = len(getCandidatesList()['body'])
##        self.test_validCandidateAdd()
##        assert (len(getCandidatesList()['body']) > init_length)
##
##    def test_deleteCandidate(self):
##        cand_id = self.test_validCandidateAdd()
##        response = deleteCandidate(cand_id)
####        print response
##        assert (response['status'] == 200)

class Candidate():
    def __init__(self, data=''):
        '''Valid by defaul'''
        if data == '':
            self.id = None
            self.name = 'name_test'
            self.position = 'pos_test'
        else:
            data_dict = json.loads(data).pop('candidate')
            self.id = data_dict['id']
            self.name = data_dict['name']
            self.position = data_dict['position']

    def body(self):
        return {'name': self.name, 'position': self.position}

    def body_id(self):
        return {'id': self.id, 'name': self.name, 'position': self.position}

    def __str__(self):
       return json.dumps({'candidate': self.body_id()})

    def __eq__(self, cand_b):
        return (self.body_id() == cand_b.body_id())

    def makeRequest(self, header={'Content-Type': 'application/json'}):
        '''Default header valid'''
        return {'body': json.dumps(self.body()),
                'header': header}

    def addId(self, id):
        self.id = id

##def getCandidatesObjList():
##    result=[]
##    candidates = json.loads(getCandidatesList()['body'])['candidates']
##    for cand_info in candidates:
##        result.append(Candidate(str(cand_info)))
##    return result

class TestVerify():
    def getCandidatesObjList(self):
        result=[]
        candidates = json.loads(getCandidatesList()['body'])['candidates']
        for cand_info in candidates:
            result.append(Candidate(cand_info))
        return result

    def test_validCandidateServerResponse(self):
        cand_a = Candidate()
        response = postCandidate(**(cand_a.makeRequest()))
        cand_id = json.loads(response['body'])['candidate']['id']
        cand_a.addId(cand_id)
        cand_b = Candidate(response['body'])
        assert (cand_a == cand_b)

##    def test_validCandidateAddWithVerif(self):
##        cand_a = Candidate()
##        response = postCandidate(**(cand_a.makeRequest()))
##        cand_id = json.loads(response['body'])['candidate']['id']
##        cand_a.addId(cand_id)
##        cand_list = self.getCandidatesObjList()
##        assert (cand_a in cand_list)
##
##    def test_validCandidateDeleteWithVerif(self):
##        body_dict = {'name': 'name_test', 'position': "pos_test"}
##        body = json.dumps(body_dict)
##        header = {'Content-Type': 'application/json'}
##        response = postCandidate(header, body)
##        cand_id = json.loads(response['body'])['candidate']['id']
##        deleteCandidate(cand_id)
##        assert (cand_id not in self.getCandidatesAsDict().keys())
##        
##    @pytest.mark.parametrize('', [[]]*10)
##    def test_randomValidCandidateGet(self):
##        candidates_dict = self.getCandidatesAsDict()
##        cand_id = random.choice(candidates_dict.keys())
##        candidate = json.loads(getCandidate(cand_id)['body'])
##        candidate_dict = {'id': cand_id}
##        candidate_dict.update(candidates_dict[cand_id])
##        assert (candidate_dict == json.loads(getCandidate(cand_id)['body'])['candidate'])        




##body_list = [json.dumps({}),
##             json.dumps({'position': "pos_test"}),
##             json.dumps({'name': "name_test"}),
##             json.dumps({'position': "P"*257}),
##             json.dumps({'name': "N"*257}),
##             json.dumps({'name': "n"*257, 'position': "p"*257})]
##header_list = [{},
##                   {'Content-Type': 'application/javascript'},
##                   {'Content-Type': 'application/json'},
##                    {'Content-Type': 'text/html'}]
##
##header_body_list = list((x,y) for x in header_list for y in body_list)
##
##def pytest_generate_tests(metafunc):
##    idlist=[]
##    argvalues=[]
##    i=0
##    try:
##        for hb_pair in metafunc.cls.header_body_list:
##           idlist.append(i)
##           argnames = ["header","body"]
##           argvalues.append(hb_pair)
##           i+=1
##        metafunc.parametrize(argnames, argvalues, ids=idlist, scope="function")
##    except:
##        pass
##
##class TestQAAdv(TestFixture):
##    header_body_list = list((x,y) for x in header_list for y in body_list)
##    
##    def test_invalidCandidateAdd(self, header, body):
##        assert (postCandidate(self.connection, header, body)['status'] == 400)
##
##    def test_invalidCandidateGet(self):
##        assert (getCandidate(self.connection, -1)['status'] == 404)
##
##    def test_invalidCandidateGet_withBH(self, header, body):
##        assert (getCandidate(self.connection, -1, header, body)['status'] == 404)
##
##    def test_invalidCandidateDelete(self):
##        assert (deleteCandidate(self.connection, -1)['status'] == 404)
##
##    def test_noCandidateDelete(self):
##        assert (deleteCandidate(self.connection, None)['status'] == 404)
##                 
##    def test_invalidCandidateDelete_withBH(self, header, body):
##        assert (deleteCandidate(self.connection, -1, header, body)['status'] == 404)
##
##    def test_validCandidateDelete_withBH(self, header, body):
##        valid_body = json.dumps({'name': 'name_test', 'position': "pos_test"})
##        valid_header = {'Content-Type': 'application/json'}
##        response = postCandidate(self.connection, valid_header, valid_body)
##        cand_id = json.loads(response['body'])['candidate']['id']
##        assert (deleteCandidate(self.connection, cand_id, header, body)['status'] == 404)
##
##    def test_deleteCandidatesList(self):
##        self.connection.request("DELETE", "/candidates")
##        response = self.connection.getresponse()
##        result = {'status':response.status, 'header':response.getheaders(), 'body':response.read()}
##        assert (result['status'], 405)

