import re

with open('src/types.ts', 'r') as f:
    content = f.read()

content = content.replace("export interface ActivityLog {\n  timestamp: string;", "export interface ActivityLog {\n  id: string;\n  timestamp: string;")

with open('src/types.ts', 'w') as f:
    f.write(content)
