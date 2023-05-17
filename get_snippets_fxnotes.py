import base64
import requests
import re
import json
import os

url = 'https://api.github.com/repos/jakobringler/blog/contents/content/notes/VEX%20Snippets.md'
req = requests.get(url)
path = "./json"

if req.status_code == requests.codes.ok:
    req = req.json() 
    content = base64.b64decode(req['content'])
else:
    print('No content found.')

infos = re.findall('\###(.*?)```', str(content))
results = re.findall('\```C(.*?)```', str(content))

for count, info in enumerate(infos):
    
    label = str(info).split("\\n//", 1)[0].lstrip(" ").replace(" ", "_")
    context = str(info).split("\\n//", 1)[1].rstrip("\\n\\n").lstrip(" ").split(" ", 1)[0].capitalize() + "s"
    data = results[count].rstrip("\\n").lstrip("\\n")
    
    dictionary ={ 
        "label": label, 
        "context": context, 
        "data": data
        } 
    
    filename = label + ".json"
    writepath = os.path.join(path, filename)
    filecontent = str(json.dumps(dictionary, indent=4)).replace("\\\\n", "\\n").replace("\\\\t", "\\t")
    
    try:
        with open(writepath, "w") as outfile:       
            outfile.write(filecontent)
    except Exception as e:
        print(e)