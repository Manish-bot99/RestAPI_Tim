import requests

BASE = "http://127.0.0.1:5000/"

# data = [{"likes": 2131, "views": 32141, "name": "video1"}, {"likes": 34242, "views": 45352, "name": "video2"},
#  {"likes": 2343, "views":54543, "name": "video3"}, {"likes": 3244, "views": 45345534, "name": "video4"},
#  {"likes": 345, "views": 555, "name": "video5"}] 

# for i in range(len(data)):
#      response = requests.put(BASE + "video/" + str(i), data[i])
#      print(response.json())

# input()
response = requests.patch(BASE + "video/1" , {"likes": 2000})
print(response.json())
# input()
# response = requests.delete(BASE + "video/2" )
# print(response)