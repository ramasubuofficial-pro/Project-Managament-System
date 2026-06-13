import re, os, glob

def fix_dark_mode():
    templates_dir = r"d:\Project Management system web app\FlaskPM\templates"
    for filepath in glob.glob(os.path.join(templates_dir, '*.html')):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Backgrounds
        content = re.sub(r'\bbg-white\b(?!/)(?!\s+dark:bg-)', r'bg-white dark:bg-navy-800', content)
        content = re.sub(r'\bbg-slate-50\b(?!/)(?!\s+dark:bg-)', r'bg-slate-50 dark:bg-navy-900', content)
        content = re.sub(r'\bbg-slate-100\b(?!/)(?!\s+dark:bg-)', r'bg-slate-100 dark:bg-navy-700', content)

        # Transparent Backgrounds
        content = re.sub(r'\bbg-white/40\b(?!\s+dark:bg-)', r'bg-white/40 dark:bg-navy-800/60', content)
        content = re.sub(r'\bbg-white/50\b(?!\s+dark:bg-)', r'bg-white/50 dark:bg-navy-800/60', content)
        content = re.sub(r'\bbg-white/60\b(?!\s+dark:bg-)', r'bg-white/60 dark:bg-navy-800/70', content)
        content = re.sub(r'\bbg-white/80\b(?!\s+dark:bg-)', r'bg-white/80 dark:bg-navy-800/80', content)

        # Text Colors
        content = re.sub(r'\btext-slate-900\b(?!\s+dark:text-)', r'text-slate-900 dark:text-white', content)
        content = re.sub(r'\btext-slate-800\b(?!\s+dark:text-)', r'text-slate-800 dark:text-white', content)
        content = re.sub(r'\btext-slate-700\b(?!\s+dark:text-)', r'text-slate-700 dark:text-slate-200', content)
        content = re.sub(r'\btext-slate-600\b(?!\s+dark:text-)', r'text-slate-600 dark:text-slate-300', content)
        content = re.sub(r'\btext-slate-500\b(?!\s+dark:text-)', r'text-slate-500 dark:text-slate-400', content)

        # Borders
        content = re.sub(r'\bborder-slate-100\b(?!\s+dark:border-)', r'border-slate-100 dark:border-navy-700', content)
        content = re.sub(r'\bborder-slate-200\b(?!\s+dark:border-)', r'border-slate-200 dark:border-navy-600', content)
        content = re.sub(r'\bborder-white/50\b(?!\s+dark:border-)', r'border-white/50 dark:border-navy-700/50', content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("Dark mode classes added to all templates.")

if __name__ == "__main__":
    fix_dark_mode()
