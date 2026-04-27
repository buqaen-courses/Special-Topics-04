# info = {} # dict()
# info['name'] = 'Amirza'
# info['version'] = 5.6
# # print(info)
# info.update(
#     {
#         "year":1396,
#         "company" : "Mehravaran Asre Danesh"
#     }
# )
# # print(info)
# from pprint import pprint 
# # pprint(info)

# info = {}
# info['name']="alireza"
# info['ver']=5.6
# # print(info)
# info.update(
# {
# "year":1396,
# "company" : "mer ariya"
# }
# )
# # print(info)
# from pprint import pprint
# info["active_versions"] = [5.6,5.5,5.4,5.2,5.0,4.3,4.2,4.1,3.8]
# pprint(info)
# # info = {}
# info["developers"] = [
#     {"name": "ali", "family" : "Ahmadi" , "role" : "Team Lead"} , 
#     {"name": "Sara", "family" : "Kamali" , "role" : "Developer"} ,
#     {"name": "Saeed", "family" : "Khazaie" , "role" : "Developer", 
#      "Desc": "Intern"} ,
#     {"name": "ahmad", "family" : "Salehi"}     
# ] 

# from pprint import pprint
# pprint(info)
# info = {'active_versions': [5.6, 5.5, 5.4, 5.2, 5.0, 4.3, 4.2, 4.1, 3.8],
#  'company': 'mer ariya',
#  'developers': [{'family': 'Ahmadi', 'name': 'ali', 'role': 'Team Lead'},
#                 {'family': 'Kamali', 'name': 'Sara', 'role': 'Developer'},
#                 {'Desc': 'Intern',
#                  'family': 'Khazaie',
#                  'name': 'Saeed',
#                  'role': 'Developer'},
#                 {'family': 'Salehi', 'name': 'ahmad'}],
#  'name': 'alireza',
#  'ver': 5.6,
#  'year': 1396}
# temp = info.copy()
# temp['company'] = 'New Company'
# pprint(info)
# k=[1,2,3]
# t = k[:]
# t[0]=100
# print(k)
# #    k   <-----Address-------        1 , 2 , 3
# # k[1] = 10
import json
person = {"name": "Alice", "age": 25}

# json_string = json.dumps(person)
# print(json_string)
# print(type(json_string))
# # json_string['name'] = 'Ali'

# print(json.dumps(person, indent=4))

# json_string = '{"name": "Alice", "age": 25}'

# person = json.loads(json_string)
# print(person["name"])    # Alice
# print(type(person))      # <class 'dict'>

# import json

# data = {
#     "name": "Alice",
#     "scores": [90, 85, 92]
# }

# with open("data.json", "w") as f:
#     json.dump(data, f, indent=4)

# number = int(input("Enter a Number (1-3) > "))

# match number:
#     case 1:
#         print("One")
#     case 2:
#         print("Two")
#     case 3:
#         print("Three")
#     case wrong:
#         print(f"Wrong Value: {wrong}")

## Output: Two


numbers = [1, 2, 3, 4, 5]
squares=[num*num for num in numbers if num % 2 ==0]
print(squares)  ## [1, 4, 9, 16, 25]

words = ["cat", "dog", "bird"]
lengths = [word[0].upper() for word in words]
print(lengths)  ## [3, 3, 4]


numbers = [-1, 0, 1, 2, -3]
is_positive = [num > 0 for num in numbers]
print(is_positive)  ## [False, False, True, True, False]


words = ["cat", "dog", "elephant", "bird"]
long_words = [word.title() for word in words if len(word) > 3]
print(long_words)




numbers = [1, 2, 2, 3, 3, 3]
squares = {num * num for num in numbers}
print(squares)  ## {1, 4, 9}


students = [
    {"name": "Alice", "grade": 90},
    {"name": "Bob",   "grade": 75},
    {"name": "Carol", "grade": 88},
]

## Get all names
names = [s["name"] for s in students]
print(names)  ## ['Alice', 'Bob', 'Carol']

## Get names of students who passed (grade >= 80)
passed = [s["name"] for s in students if s["grade"] >= 80]
print(passed)  ## ['Alice', 'Carol']






