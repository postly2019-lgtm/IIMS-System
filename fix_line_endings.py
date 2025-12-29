import os

files = ['startup.sh', 'build.sh', 'Procfile', 'requirements.txt']

for filename in files:
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            content = f.read()
        
        # Replace CRLF with LF
        new_content = content.replace(b'\r\n', b'\n')
        
        if new_content != content:
            print(f"Fixing line endings for {filename}")
            with open(filename, 'wb') as f:
                f.write(new_content)
        else:
            print(f"{filename} already has LF line endings")
