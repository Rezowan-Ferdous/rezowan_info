
import json
from sqlalchemy import create_engine, text
from datetime import datetime, date

# Configuration
DB_URI = 'postgresql://postgres:Rez.7890@localhost/rezowan_info'

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def export_data():
    engine = create_engine(DB_URI)
    data = {}
    
    with engine.connect() as conn:
        print("Exporting Projects...")
        projects = conn.execute(text("SELECT * FROM project")).mappings().all()
        data['projects'] = [dict(row) for row in projects]
        
        print("Exporting Publications...")
        publications = conn.execute(text("SELECT * FROM publication ORDER BY year DESC")).mappings().all()
        data['publications'] = [dict(row) for row in publications]
        
        print("Exporting Blog Posts...")
        posts = conn.execute(text("SELECT * FROM blog_post ORDER BY date_posted DESC")).mappings().all()
        data['posts'] = [dict(row) for row in posts]
        
        print("Exporting Experience...")
        experience = conn.execute(text("SELECT * FROM experience ORDER BY start_date DESC")).mappings().all()
        data['experience'] = [dict(row) for row in experience]
        
    with open('site_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, default=json_serial, indent=4)
        
    print("Data exported to site_data.json")

if __name__ == "__main__":
    export_data()
