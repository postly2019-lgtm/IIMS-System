import os

files = ['startup.sh', 'Procfile', 'requirements.txt', 'runtime.txt']

for filename in files:
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            content = f.read()
        
        # Force conversion of CRLF to LF
        content = content.replace(b'\r\n', b'\n')
        
        with open(filename, 'wb') as f:
            f.write(content)
        print(f"Fixed line endings for {filename}")
