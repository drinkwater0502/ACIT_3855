import json

file_handle = open('data.json', 'r')
file_contents = file_handle.read()
python_data = json.loads(file_contents) #convert json string to python data (array)
print(python_data)
file_handle.close()