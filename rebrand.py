import os

search_dir = r"d:\Project Management system web app\FlaskPM"
extensions = ('.html', '.py', '.js', '.json', '.md')

replacements = [
    ("ACCIO HUB", "ACCIO HUB"),
    ("Accio Hub", "Accio Hub"),
    ("acciohub", "acciohub"),
    ("navy-", "navy-"),
    ("gold-", "gold-"),
    ("accio_logo.png", "accio_logo.png")
]

for root, _, files in os.walk(search_dir):
    if "venv" in root or ".git" in root or "__pycache__" in root:
        continue
    for file in files:
        if file.endswith(extensions):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for old, new in replacements:
                    new_content = new_content.replace(old, new)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {file_path}")
            except Exception as e:
                print(f"Could not process {file_path}: {e}")

print("Rebrand replacements complete!")
