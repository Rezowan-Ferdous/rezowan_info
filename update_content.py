
import json
from datetime import datetime

data = {
    "projects": [],  # Keeping empty as per previous state, user can add later
    "posts": [
        {
            "id": 1,
            "title": "Welcome to my new Blog",
            "slug": "welcome-blog",
            "content": "<p>This is the first post on my new blog system!</p>",
            "date_posted": datetime.now().isoformat()
        }
    ],
    "publications": [
        # Journals
        {
            "id": "j1",
            "title": "Deep Learning and Attention-Based Methods for Human Activity Recognition and Anticipation: A Review",
            "authors": "Rezowan Shuvo, et al.",
            "venue": "Cognitive Computation (Springer, Q1)",
            "year": 2025,
            "link": "https://link.springer.com/article/10.1007/s12559-025-10513-2",
            "pub_type": "Journal (Q1)",
            "abstract": "A comprehensive review of deep learning and attention-based methods for human activity recognition and anticipation."
        },
        {
            "id": "j2",
            "title": "MSBATN: Multi-Stage Boundary-Aware Transformer Network for action segmentation in untrimmed surgical videos",
            "authors": "Rezowan Shuvo, MS Mekala, Eyad Elyan",
            "venue": "Computer Vision and Image Understanding (Elsevier, Q1)",
            "year": 2025,
            "link": "https://www.sciencedirect.com/science/article/abs/pii/S1077314225002449",
            "pub_type": "Journal (Q1)",
            "abstract": "Proposing a Multi-Stage Boundary-Aware Transformer Network for precise action segmentation in surgical videos."
        },
        {
            "id": "j3",
            "title": "Deep Learning Models for the Diagnosis and Screening of COVID-19: A Systematic Review",
            "authors": "Rezowan Shuvo, et al.",
            "venue": "SN Computer Science (Springer, Q2)",
            "year": 2022,
            "link": "https://pubmed.ncbi.nlm.nih.gov/35911439/",
            "pub_type": "Journal",
            "abstract": "A systematic review of deep learning models used for COVID-19 diagnosis and screening from medical imaging."
        },
        # Conferences
        {
            "id": "c1",
            "title": "GPAT: Goal-Progression-Aware Transformer with Recursive Grammar Induction for Action Anticipation",
            "authors": "Rezowan Shuvo, MS Mekala, Eyad Elyan",
            "venue": "European Conference on Computer Vision (ECCV) (Rank A*)",
            "year": 2024,
            "link": "#",
            "pub_type": "Conference",
            "abstract": "(Submitted)"
        },
        {
            "id": "c2",
            "title": "Chirality-Aware Grammar-Guided Surgical Action Anticipation from Video",
            "authors": "Rezowan Shuvo, MS Mekala, Eyad Elyan",
            "venue": "Human Robotic Interactions (HRI) (Rank A)",
            "year": 2026,
            "link": "#",
            "pub_type": "Conference",
            "abstract": "(Accepted)"
        },
        {
            "id": "c3",
            "title": "Performance Analysis of Different Loss Function in Face Detection Architectures",
            "authors": "Rezowan Hossain Ferdous, et al.",
            "venue": "International Conference on Trends in Computational and Cognitive Engineering, Dhaka",
            "year": 2020,
            "link": "#",
            "pub_type": "Conference",
            "abstract": ""
        }
    ],
    "experience": [
        {
            "id": 1,
            "position": "PhD Candidate and Teaching Assistant",
            "company": "Robert Gordon University",
            "location": "Aberdeen, Scotland",
            "start_date": "2023-03-01",
            "end_date": None,
            "description": "• Conducting advanced research on complex surgical video understanding, focusing on spatial-temporal context analysis.<br>• Developing frameworks for future action prediction and safety evaluation to detect potential surgical errors.<br>• Implementing novel architectures using Vision Transformers and State Space Models (SSM) for segmentation and detection tasks.<br>• Pioneering the application of Large Language Models (LLMs) and Vision-Language Models (VLMs) to enhance visual reasoning for complex robotic tasks.<br>• Teaching students; conducted labs on Python programming, Data Science, and NLP."
        },
        {
            "id": 2,
            "position": "Software Developer",
            "company": "Beraten Software Corporation",
            "location": "Portland, OR-USA (Remote)",
            "start_date": "2022-05-01",
            "end_date": "2023-03-01",
            "description": "• Engineered software solutions for Indian Child Welfare and Tribal Court systems using .NET Core 6 Framework and MSSQL Server.<br>• Developed and maintained e-court systems for criminal case management, ensuring robust data handling and security.<br>• Managed project version control and collaboration using Bitbucket and GitHub.<br>• Integrated complex database schemas with .NET backend services to support tribal healthcare and welfare services."
        },
        {
            "id": 3,
            "position": "Research Assistant",
            "company": "Time Research and Innovation (TRI)",
            "location": "Southampton, UK (Dhaka Branch)",
            "start_date": "2020-10-01",
            "end_date": "2022-10-01",
            "description": "• Conducted research projects and led the Software Development Life Cycle (SDLC) in collaboration with developers.<br>• Assisted in system designing and requirement engineering to align technical outputs with research goals.<br>• Developed and deployed an end-to-end facial recognition system for smart attendance with MLOps.<br>• Analyzed chest X-ray data for COVID-19 detection using deep learning models."
        }
    ],
    "skills": {
        "Programming": ["Python", "C# (.NET Core)", "Bash", "SQL"],
        "MLOps Tools": ["Docker", "CI/CD", "Git", "Packaging", "Pytest", "Version Control", "Bitbucket"],
        "Tools & Platforms": ["Raspberry Pi", "Overleaf", "MSSQL Server", "MATLAB", "ROS", "Arduino"],
        "Deep Learning & ML": ["PyTorch", "TensorFlow", "Keras", "Hugging Face", "Scikit-learn", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn"],
        "Mathematics": ["Linear Algebra", "Calculus", "Probability", "Statistics"],
        "AI & Analytics": ["Data Analytics", "Machine Learning (ML)", "Deep Learning (DL)", "AI", "Classification", "Regression", "Object Detection", "Predictive Analysis"],
        "Soft Skills": ["Project Management", "Business & Data-Driven Decision Making", "Communication", "Team Collaboration"],
        "Research Interests": ["Predictive Analysis", "Robotics (Vision)", "Action Analysis", "Video Analysis", "Inspections", "Reasoning"]
    },
    "awards": [
        {
            "title": "PhD Studentship",
            "year": "2023",
            "organization": "Robert Gordon University",
            "description": "Fully funded PhD scholarship awarded by the School of Computing Engineering and Technology."
        },
        {
            "title": "Employee of the Month",
            "year": "2021",
            "organization": "Time Research and Innovation (TRI)",
            "description": "Recognized for outstanding performance and contributions to research development."
        }
    ],
    "volunteering": [
        {
            "role": "Reviewer",
            "period": "Jun 2024 – Present",
            "organization": "IEEE Transactions on Neural Networks and Learning Systems",
            "description": "Reviewing technical manuscripts and providing constructive feedback."
        },
        {
            "role": "Volunteer",
            "period": "May 2025 – Present",
            "organization": "Active School Aberdeen, Scotland",
            "description": "Engaging in voluntary sessions to support school activities."
        }
    ],
    "references": [
        {
            "name": "Eyad Elyan",
            "title": "Professor, Robert Gordon University",
            "email": "e.elyan@rgu.ac.uk"
        },
        {
            "name": "Md Junayed Hasan",
            "title": "AI Engineer, Subsea7",
            "email": "junayed.hasan@subsea7.com"
        },
        {
            "name": "Dr. M Shamim Kaiser",
            "title": "Professor, Jahangirnagar University, Dhaka",
            "email": "mskaiser@juniv.edu"
        }
    ]
}

with open('site_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
print("Updated site_data.json with user content")
