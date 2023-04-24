import os
import json
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

for root, dirs, files in os.walk("fhir_resources", topdown=False):
       for name in files:
            if name.endswith(".json"):
               resource_type, _ = name.split('-',1)
               with open(os.path.join(root, name)) as f:
                    jf = json.load(f)
                    resource_id = jf['id']
                    redis_id = f"{resource_type}:{resource_id}"
                    r.set(redis_id, json.dumps(jf))
                    print(resource_type,':',resource_id)

