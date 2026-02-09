
import os
import shutil
from jinja2 import Environment, FileSystemLoader
import json
from datetime import datetime

# Configuration
TEMPLATE_DIR = '_templates'
OUTPUT_DIR = '.' # Root directory
DATA_FILE = 'site_data.json'

# Setup Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Convert date strings back to objects
    for post in data['posts']:
        post['date_posted'] = datetime.fromisoformat(post['date_posted'])
        
    for exp in data['experience']:
        exp['start_date'] = datetime.fromisoformat(exp['start_date'])
        if exp['end_date']:
            exp['end_date'] = datetime.fromisoformat(exp['end_date'])
            
    return data

def render(template_name, context, output_path):
    # Calculate relative root
    # Normalize path separators
    rel_path = os.path.relpath(output_path, OUTPUT_DIR)
    depth = len(rel_path.split(os.sep)) - 1
    relative_root = '../' * depth if depth > 0 else '.'
    
    # Remove trailing slash from relative_root if it's not just '.'
    if relative_root.endswith('/') and relative_root != './':
        relative_root = relative_root.rstrip('/')
        
    context['relative_root'] = relative_root

    template = env.get_template(template_name)
    content = template.render(**context)
    
    # Ensure directory exists
    dir_name = os.path.dirname(output_path)
    if dir_name:
        if os.path.isfile(dir_name):
            os.remove(dir_name) # Remove file if it blocks directory creation
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            
    # Check if target is a directory (should be a file)
    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {output_path}")

def build():
    print("Starting build...")
    
    try:
        data = load_data()
    except FileNotFoundError:
        print(f"Error: {DATA_FILE} not found. Run export_data.py first.")
        return

    projects = data.get('projects', [])
    publications = data.get('publications', [])
    posts = data.get('posts', [])
    experience = data.get('experience', [])
    skills = data.get('skills', {})
    awards = data.get('awards', [])
    volunteering = data.get('volunteering', [])
    references = data.get('references', [])
        
    # Prepare Contexts
    latest_posts = posts[:1]
    selected_pubs = publications[:1]
    
    # 1. Home
    render('home.html', {
        'title': 'Home',
        'active_page': 'home',
        'latest_posts': latest_posts,
        'selected_pubs': selected_pubs,
        'latest_projects': projects[:1],
        'experience': experience,
        'skills': skills,
        'awards': awards,
        'volunteering': volunteering,
        'references': references
    }, os.path.join(OUTPUT_DIR, 'index.html'))
    
    # 2. Projects
    render('projects.html', {
        'title': 'Projects',
        'active_page': 'projects',
        'projects': projects
    }, os.path.join(OUTPUT_DIR, 'projects.html')) 
    
    # 3. Research
    journals = [p for p in publications if p.get('pub_type') in ['Journal', 'Journal (Q1)']]
    conferences = [p for p in publications if p.get('pub_type') not in ['Journal', 'Journal (Q1)']]
    
    render('research.html', {
        'title': 'Research',
        'active_page': 'research',
        'journals': journals,
        'conferences': conferences
    }, os.path.join(OUTPUT_DIR, 'research.html'))
    
    # 4. Blog Index
    render('blog.html', {
        'title': 'Blog',
        'active_page': 'blog',
        'posts': posts
    }, os.path.join(OUTPUT_DIR, 'blog.html'))
    
    # 5. Detail Pages - Projects
    for proj in projects:
        render('project_detail.html', {
            'title': proj['title'],
            'active_page': 'projects',
            'project': proj
        }, os.path.join(OUTPUT_DIR, 'project', str(proj['id']), 'index.html'))
        
    # 6. Detail Pages - Publications
    for pub in publications:
        if pub.get('abstract') and pub['abstract'].strip():
            render('publication_detail.html', {
                'title': pub['title'],
                'active_page': 'research',
                'publication': pub
            }, os.path.join(OUTPUT_DIR, 'research', str(pub['id']), 'index.html'))
        
    # 7. Detail Pages - Blog Posts
    for post in posts:
        render('post_detail.html', {
            'title': post['title'],
            'active_page': 'blog',
            'post': post
        }, os.path.join(OUTPUT_DIR, 'blog', post['slug'], 'index.html'))

    print("Build complete.")

if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print(f"Build failed: {e}")
        import traceback
        traceback.print_exc()
