import os
import glob
import re

directory = "/root/artha/backend/app/api/v1"

for filepath in glob.glob(os.path.join(directory, "*.py")):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace @router.get("/") with @router.get("")
    content = re.sub(r'@router\.get\("/"\)', '@router.get("")', content)
    # Replace @router.post("/") with @router.post("")
    content = re.sub(r'@router\.post\("/"\)', '@router.post("")', content)
    # Replace @router.put("/") with @router.put("")
    content = re.sub(r'@router\.put\("/"\)', '@router.put("")', content)

    with open(filepath, 'w') as f:
        f.write(content)

print("Fixed trailing slashes!")
