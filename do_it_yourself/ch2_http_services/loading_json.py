import json

text_json = '''{
    "demo": "Processing JSON in Python",
    "instructor": "Michael",
    "duration": "5.0"
    }'''

print(type(text_json), text_json)
print()

data = json.loads(text_json)

print(type(data), data)
print()

# instructor = data['instructor']
instructor = data.get('instructor', 'SUBSTITUTE')
print("Your instructor is {}".format(instructor))

data['instructor'] = 'Jeff'

new_json = json.dumps(data)

instructor = data.get('instructor')

print("Your instructor is {}".format(instructor))