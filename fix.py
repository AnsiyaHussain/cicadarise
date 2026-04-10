import os

base_dir = r'c:\Users\siyaa\OneDrive\Documents\cicada\CICADA\app\templates'
files = ['index.html', 'product.html', 'contact.html']

for file in files:
    path = os.path.join(base_dir, file)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the literal backslash and quote with just the quote
        content = content.replace(r"\'contact\'", "'contact'")
        content = content.replace(r"\'product\'", "'product'")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

print('Fixed quotes in templates.')
