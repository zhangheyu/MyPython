import json

json_data = '[{"ID":10,"Name":"Pankaj","Role":"CEO"},' \
            '{"ID":20,"Name":"David Lee","Role":"Editor"}]'

json_object = json.loads(json_data)

json_formatted_str = json.dumps(json_object, indent=2)

# print(json_formatted_str)


root = {}
path_dict = {
  "/": {
    "{{END}}": "/"
  },
  "/aa": {
    "{{END}}": "/aa",
    "/": {
      "{{END}}": "/aa/"
    }
  },
  "/bb": {
    "{{SUB_TREE}}": {
      "{{END}}": "/bb/*"
    },
    "{{END}}": "/bb"
  },
  "/cc": {
    "{{ANY}}": {
      "/profile": {
        "{{END}}": "/cc/{id}/profile"
      }
    },
    'cc': 'ccccccc'
  },
  "/cl": {
        "{{ANY}}": {
            "/profile": {
                "{{END}}": "/cl/{id}/profile"
            }
        },
        'cc': 'ccccc'
    }
}

for path, val in path_dict.items():
    print('path:', path)
    # print('value:', val)

    if not path:
        assert (False)

    tree = path_dict

    if path.startswith('/c'):
        tree = val
    if 'cc' in tree:
        tree['cc'] = 'repeat'

print(json.dumps(path_dict, indent=2))


result = dict(records='records', column_names='column_names',
              column_types='column_types')
print(result)

paths = ['one: 1', 'two: 2', 'three: 3']
data = {}
[data.update({k: v}) for k, v in paths]

print(json.dumps(data, indent=2))
