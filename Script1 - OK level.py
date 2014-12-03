import httplib, unittest, json

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

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.connection = httplib.HTTPConnection("qainterview.cogniance.com")
        try:
            self.connection.connect()
        except:
            raise Exception("Connection error")

        self.body_list = [json.dumps({}),
                     json.dumps({'position': "pos_test"}),
                     json.dumps({'name': "name_test"}),
                     json.dumps({'position': "P"*257}),
                     json.dumps({'name': "N"*257}),
                     json.dumps({'name': "n"*257, 'position': "p"*257})]
        self.header_list = [{},
                           {'Content-Type': 'application/javascript'},
                           {'Content-Type': 'application/json'},
                            {'Content-Type': 'text/html'}]

        self.longmessage = True

    def tearDown(self):
        self.connection.close()

class GetTest(SimpleTest):
    def test_getCandidatesList(self):
        self.assertEqual(getCandidatesList(self.connection)['status'], 200, 'GET test fail')

    def test_validCandidateAdd(self):
        body = json.dumps({'name': 'name_test', 'position': "pos_test"})
        header = {'Content-Type': 'application/json'}
        response = postCandidate(self.connection, header, body)
        self.assertEqual(response['status'], 201, 'POST test fail')
##        print response
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
        response = deleteCandidate(self.connection, cand_id)
##        print response
        self.assertEqual(response['status'], 200)


class AdvTest(SimpleTest):
       
    def test_invalidCandidateAdd(self):
        header_body_list = list((x,y) for x in self.header_list for y in self.body_list)
        for hb_pair in header_body_list:
            self.assertEqual(postCandidate(self.connection, *hb_pair)['status'], 400, str(hb_pair))

    def test_invalidCandidateGet(self):
        self.assertEqual(getCandidate(self.connection, -1)['status'], 404)

    def test_invalidCandidateGet_withBH(self):
        header_body_list = list((x,y) for x in self.header_list for y in self.body_list)
        for hb_pair in header_body_list:
            self.assertEqual(getCandidate(self.connection, -1, *hb_pair)['status'], 404, str(hb_pair))

    def test_invalidCandidateDelete(self):
        self.assertEqual(deleteCandidate(self.connection, -1)['status'], 404)

    def test_noCandidateDelete(self):
        self.assertEqual(deleteCandidate(self.connection, None)['status'], 404)
                 
    def test_invalidCandidateDelete_withBH(self):
        header_body_list = list((x,y) for x in self.header_list for y in self.body_list)
        for hb_pair in header_body_list:
            self.assertEqual(deleteCandidate(self.connection, -1, *hb_pair)['status'], 404, str(hb_pair))

    def test_validCandidateDelete_withBH(self):
        body = json.dumps({'name': 'name_test', 'position': "pos_test"})
        header = {'Content-Type': 'application/json'}
        response = postCandidate(self.connection, header, body)
        cand_id = json.loads(response['body'])['candidate']['id']
        header_body_list = list((x,y) for x in self.header_list for y in self.body_list)[1:]
        for hb_pair in header_body_list:
            self.assertEqual(deleteCandidate(self.connection, cand_id, *hb_pair)['status'], 404, str(hb_pair))

    def test_deleteCandidatesList(self):
        self.connection.request("DELETE", "/candidates")
        response = self.connection.getresponse()
        result = {'status':response.status, 'header':response.getheaders(), 'body':response.read()}
        self.assertEqual(result['status'], 405)
            

suite = unittest.TestLoader().loadTestsFromTestCase(GetTest)
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(AdvTest))
unittest.TextTestRunner(verbosity=2).run(suite)


