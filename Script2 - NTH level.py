import json, requests, random, pytest

def getCandidate(cand_id = None, header={}, body=""):
    if cand_id:
        response = requests.get('http://qainterview.cogniance.com/candidates/'+str(cand_id),
                                data = body,
                                headers = header)
    else:
        response = requests.get('http://qainterview.cogniance.com/candidates',
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

class Candidate():
    def __init__(self, data=''):
        '''Valid by defaul'''
        if data == '':
            self.id = None
            self.name = 'name_test'
            self.position = 'pos_test'
        else:            
            if (type(data) == 'str') or (type(data) == type(u'')):
                data_dict = json.loads(data).pop('candidate')
                self.id = data_dict['id']
                self.name = data_dict['name']
                self.position = data_dict['position']
            else:
                self.id = data['id']
                self.name = data['name']
                self.position = data['position']

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


class TestVerify():
    def getCandidatesObjList(self):
        result=[]
        candidates = json.loads(getCandidate()['body'])['candidates']
        for cand_info in candidates:
            result.append(Candidate(cand_info))
        return result

    def getCandidatesIdList(self):
        result=[]
        candidates = json.loads(getCandidate()['body'])['candidates']
        for cand_info in candidates:
            result.append(Candidate(cand_info)['id'])
        return result

    def test_validCandidateServerResponse(self):
        cand_a = Candidate()
        response = postCandidate(**(cand_a.makeRequest()))
        cand_id = json.loads(response['body'])['candidate']['id']
        cand_a.addId(cand_id)
        cand_b = Candidate(response['body'])
        assert (cand_a == cand_b)


    def test_validCandidateAddWithVerif(self):
        cand_a = Candidate()
        response = postCandidate(**(cand_a.makeRequest()))
        cand_id = json.loads(response['body'])['candidate']['id']
        cand_a.addId(cand_id)
        cand_list = self.getCandidatesObjList()
        assert (cand_a in cand_list)

    def test_validCandidateGetWithVerif(self):
        cand_a = Candidate()
        response = postCandidate(**(cand_a.makeRequest()))
        cand_id = json.loads(response['body'])['candidate']['id']
        cand_a.addId(cand_id)
        response = getCandidate(cand_id)
        cand_b = Candidate(response['body'])
        assert (cand_a == cand_b)

    def test_validCandidateDeleteWithVerif(self):
        cand_a = Candidate()
        response = postCandidate(**(cand_a.makeRequest()))
        cand_id = json.loads(response['body'])['candidate']['id']
        cand_a.addId(cand_id)
        
        response = deleteCandidate(cand_id)
        deleteCandidate(cand_id)
        cand_list = self.getCandidatesObjList()
        assert (cand_a not in cand_list)
        
    @pytest.mark.parametrize('', [[]]*10)
    def test_randomValidCandidateGet(self):
        cands = self.getCandidatesObjList()
        cand_a = random.choice(cands)
        response = getCandidate(cand_a.id)
        cand_b = Candidate(response['body'])
        assert (cand_a == cand_b)        


if __name__ == '__main__':
    pytest.main([__file__, '-v',"--capture=sys"])
