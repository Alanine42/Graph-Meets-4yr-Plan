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
    



