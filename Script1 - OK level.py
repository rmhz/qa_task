import httplib, unittest, json

def getCandidatesList(connection):
    connection.request("GET", "/candidates")
    response = connection.getresponse()
    return {'status':response.status, 'header':response.getheaders(), 'body':response.read()}

def getCandidate(connection, cand_id):
    connection.request("GET", "/candidates/"+str(cand_id))
    response = connection.getresponse()
    return {'status':response.status, 'header':response.getheaders(), 'body':response.read()}

def postCandidate(connection, header, body):
    connection.request("POST", "/candidates", body, header)
    response = connection.getresponse()
    return {'status':response.status, 'header':response.getheaders(), 'body':response.read()}

def deleteCandidate(connection, cand_id):
    connection.request("DELETE", "/candidates/"+str(cand_id))
    response = connection.getresponse()
    return {'status':response.status, 'header':response.getheaders(), 'body':response.read()}    

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.connection = httplib.HTTPConnection("qainterview.cogniance.com")
        try:
            self.connection.connect()
        except:
            raise Exception("Connection error")

    def tearDown(self):
        self.connection.close()

class GetTest(SimpleTest):
    def test_getCandidatesList(self):
        self.assertEqual(getCandidatesList(self.connection)['status'], 200, 'GET test fail')

    def test_validCandidateAdd(self):
        body = json.dumps({'name': "name_test", 'position': "pos_test"})
        header = {'Content-Type': 'application/json'}
        response = postCandidate(self.connection, header, body)
        self.assertEqual(response['status'], 201, 'POST test fail')
        return json.loads(response['body'])['candidate']['id']

    def test_getCandidate(self):
        cand_id = self.test_validCandidateAdd()
        self.assertEqual(getCandidate(self.connection, cand_id)['status'], 200)

    def test_dataAddedToServer(self):
        init_length = len(getCandidatesList(self.connection)['body'])
        self.test_validCandidateAdd()
        self.assertGreater(len(getCandidatesList(self.connection)['body']), init_length)
    
    def test_deleteCandidate(self):
        cand_id = self.test_validCandidateAdd()
        self.assertEqual(deleteCandidate(self.connection, cand_id)['status'], 200)

if __name__ == '__main__':
    unittest.main()
