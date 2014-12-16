import httplib, pytest, json

def getCandidatesList(connection, header={}, body=""):
    connection.request("GET", "/candidates", body, header)
    response = connection.getresponse()
    return {'status':response.status, 'header':response.getheaders(), 'body':response.read()}

def getCandidate(connection, cand_id, header={}, body=""):
    connection.request("GET", "/candidates/"+str(cand_id), body, header)
    response = connection.getresponse()
    return {'status':response.status, 'header':response.getheaders(), 'body':response.read()}

def postCandidate(connection, header, body):
    connection.request("POST", "/candidates", body, header)
    response = connection.getresponse()
    return {'status':response.status, 'header':response.getheaders(), 'body':response.read()}

def deleteCandidate(connection, cand_id, header={}, body=""):
    connection.request("DELETE", "/candidates/"+str(cand_id), body, header)
    response = connection.getresponse()
    return {'status':response.status, 'header':response.getheaders(), 'body':response.read()}    


class TestFixture():
    def setup_method(self, method):
        self.connection = httplib.HTTPConnection("qainterview.cogniance.com")
        try:
            self.connection.connect()
        except:
            raise Exception("Connection error")

    def teardown_method(self, method):
        self.connection.close()

class TestQA(TestFixture):
    def test_getCandidatesList(self):
        assert (getCandidatesList(self.connection)['status'] == 200)

    def test_validCandidateAdd(self):
        body = json.dumps({'name': 'name_test', 'position': "pos_test"})
        header = {'Content-Type': 'application/json'}
        response = postCandidate(self.connection, header, body)
        assert (response['status'] == 201)
        return json.loads(response['body'])['candidate']['id']

    def test_getCandidate(self):
        cand_id = self.test_validCandidateAdd()
        assert (getCandidate(self.connection, cand_id)['status'] == 200)

    def test_dataAddedToServer(self):
        init_length = len(getCandidatesList(self.connection)['body'])
        self.test_validCandidateAdd()
        assert (len(getCandidatesList(self.connection)['body']) > init_length)

    def test_deleteCandidate(self):
        cand_id = self.test_validCandidateAdd()
        response = deleteCandidate(self.connection, cand_id)
##        print response
        assert (response['status'] == 200)

body_list = [json.dumps({}),
             json.dumps({'position': "pos_test"}),
             json.dumps({'name': "name_test"}),
             json.dumps({'position': "P"*257}),
             json.dumps({'name': "N"*257}),
             json.dumps({'name': "n"*257, 'position': "p"*257})]
header_list = [{},
                   {'Content-Type': 'application/javascript'},
                   {'Content-Type': 'application/json'},
                    {'Content-Type': 'text/html'}]

header_body_list = list((x,y) for x in header_list for y in body_list)

def pytest_generate_tests(metafunc):
    idlist=[]
    argvalues=[]
    i=0
    try:
        for hb_pair in metafunc.cls.header_body_list:
           idlist.append(i)
           argnames = ["header","body"]
           argvalues.append(hb_pair)
           i+=1
        metafunc.parametrize(argnames, argvalues, ids=idlist, scope="function")
    except:
        pass

class TestQAAdv(TestFixture):
    header_body_list = list((x,y) for x in header_list for y in body_list)
    
    def test_invalidCandidateAdd(self, header, body):
        assert (postCandidate(self.connection, header, body)['status'] == 400)

    def test_invalidCandidateGet(self):
        assert (getCandidate(self.connection, -1)['status'] == 404)

    def test_invalidCandidateGet_withBH(self, header, body):
        assert (getCandidate(self.connection, -1, header, body)['status'] == 404)

    def test_invalidCandidateDelete(self):
        assert (deleteCandidate(self.connection, -1)['status'] == 404)

    def test_noCandidateDelete(self):
        assert (deleteCandidate(self.connection, None)['status'] == 404)
                 
    def test_invalidCandidateDelete_withBH(self, header, body):
        assert (deleteCandidate(self.connection, -1, header, body)['status'] == 404)

    def test_validCandidateDelete_withBH(self, header, body):
        valid_body = json.dumps({'name': 'name_test', 'position': "pos_test"})
        valid_header = {'Content-Type': 'application/json'}
        response = postCandidate(self.connection, valid_header, valid_body)
        cand_id = json.loads(response['body'])['candidate']['id']
        assert (deleteCandidate(self.connection, cand_id, header, body)['status'] == 404)

    def test_deleteCandidatesList(self):
        self.connection.request("DELETE", "/candidates")
        response = self.connection.getresponse()
        result = {'status':response.status, 'header':response.getheaders(), 'body':response.read()}
        assert (result['status'] == 405)

if __name__ == '__main__':
    pytest.main([__file__, '-v',"--capture=sys"])
