from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
import json

@api_view(['GET'])
def getTrie(request):
    with open(os.path.dirname(__file__)+'/../../trie.json', 'r') as f:
        trie = json.load(f)
        return Response(trie)
    

@api_view(['GET'])
def getIndex(request):
    with open(os.path.dirname(__file__)+'/../../index.json', 'r') as f:
        data = json.load(f)
        return Response(data)
    
    
# Full Name
# Description
# Prerequisites: [cID]
# Unlocks:  [cID]
@api_view(['GET'])
def getPrereqs(request):
    with open(os.path.dirname(__file__)+'/../../prereqsSuccint.json', 'r') as f:
        data = json.load(f)
        return Response(data)

@api_view(['GET'])
def getCourseDetail(request, cID): 
    with open(os.path.dirname(__file__)+'/../../mongodb_crawler/courseObjects.json', 'r') as f:
        # O(N)
        for line in f:
            courseObject = json.loads(line)
            # CSE-110
            if courseObject['cID'].split() == cID.split('_'):
                data = {}
                data['name'] = courseObject['cName']
                data['description'] = courseObject['cDescription']
                return Response(data)
        
    
