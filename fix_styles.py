import os, re

folder = 'C:/Users/siyaa/OneDrive/Documents/cicada/color changed/old_cicada template/CICADA/app/templates'

for d, _, fs in os.walk(folder):
    for f in fs:
        if f.endswith('.html'):
            path = os.path.join(d, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Remove inline color and background-color declarations
            content = re.sub(r'color:\s*#[0-9a-fA-F]{3,6}\s*;?', '', content)
            content = re.sub(r'background(?:-color)?:\s*#[0-9a-fA-F]{3,6}\s*;?', '', content)
            
            # Map specific CSS variables to standard theme ones
            content = content.replace('var(--dark-brown)', 'var(--heading-color)')
            content = content.replace('var(--accent)', 'var(--bs-primary)')
            content = content.replace('var(--deep-brown)', 'var(--bs-primary)')
            
            # Generalize fonts
            content = content.replace('\"Marcellus\", serif', 'var(--heading-font)')
            content = content.replace('\'Marcellus\', serif', 'var(--heading-font)')
            content = content.replace('\"Georgia\", serif', 'var(--heading-font)')
            content = content.replace('\'Georgia\', serif', 'var(--heading-font)')

            # Clean empty style tags
            content = content.replace('style=\"\"', '')
            content = content.replace('style=\" \"', '')

            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)

print('Done cleaning all inline color styles!')
