import os
from bs4 import BeautifulSoup

# Configuration
FRONTEND_DIR = r"c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend"

def audit_file(filepath):
    if not filepath.endswith(".html"):
        return None

    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 1. Check for garbage residues
        garbage_patterns = ['dY', 'Â', 'Ã', '']
        for p in garbage_patterns:
            if p in content:
                issues.append(f"Contains residue: {p}")
        
        # 2. Check for H1
        if not soup.find('h1'):
            issues.append("Missing H1 tag")
            
        # 3. Check for Meta Description
        if not soup.find('meta', attrs={'name': 'description'}):
            issues.append("Missing Meta Description")
            
        # 4. Check for SEO Expansion block (Protocol Specification)
        # We manually expand 2 blogs and the master registry, 
        # and use the expander for tool pages.
        # Let's check for 'Protocol Specification' or 'FAQ' in tool pages.
        filename = os.path.basename(filepath)
        if filename not in ['index.html', 'all-tools.html', 'about.html', 'contact.html', 'privacy-policy.html', 'terms-of-service.html', 'error.html']:
            if 'Protocol Specification' not in content and 'FAQ' not in content:
                issues.append("Missing SEO FAQ/Protocol block")

        return issues if issues else None
    except Exception as e:
        return [f"Audit Error: {e}"]

def main():
    report = {}
    for root, dirs, files in os.walk(FRONTEND_DIR):
        # Skip blog directory if needed, or include it
        for file in files:
            res = audit_file(os.path.join(root, file))
            if res:
                report[file] = res
                
    if report:
        print("SEO/Integrity Audit Report:")
        for file, issues in report.items():
            print(f"[{file}]")
            for issue in issues:
                print(f"  - {issue}")
    else:
        print("All laboratory assets passed the SEO/Integrity Audit.")

if __name__ == "__main__":
    main()
