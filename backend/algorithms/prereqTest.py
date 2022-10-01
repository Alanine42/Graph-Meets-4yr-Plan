import json

def trimPrerequisitesRawData():
    prereqSuccint = {}
    with open('prereqs.json', 'r') as f:
        arr = json.load(f)
        for d in arr:
            name = d['course']
            newPrereqs = []
            for lst in d['prereqs']:
                newPrereqs.append([x['course'] for x in lst])
            prereqSuccint[name] = newPrereqs
        
        with open('prereqsSuccint.json', 'w') as o:
            json.dump(prereqSuccint, o)

trimPrerequisitesRawData()
    
# def workingWithRawData():
#     def binarySearch(arr, name):
#         lo, hi = 0, len(arr)
#         while lo < hi:
#             mid = (lo+hi)//2
#             midName = arr[mid]['course']
        
#             if name > midName:
#                 lo = mid+1
#             elif name < midName:
#                 hi = mid-1
#             else:
#                 return arr[mid]            
            
#         # Is arr[lo] the one you wanted?
#         if arr[lo]['course'] == name:
#             return arr[lo]

#     with open('prereqs.json', 'r') as f:
#         arr = json.load(f)
#         arr.sort(key=lambda x: x['course'])
        
#         with open('prereqsSorted.json', 'w') as o:
#             json.dump(arr, o, indent=4)
            
#         obj = binarySearch(arr, 'ECON 175')