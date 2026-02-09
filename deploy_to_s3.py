import boto3
import os
import mimetypes

# Configuration
BUCKET_NAME = "rezowan.com"  # Replace with your actual bucket name
BUILD_DIR = "."  # We are deploying from the root where build.py runs

def deploy():
    s3 = boto3.client('s3')
    
    print(f"Deploying to {BUCKET_NAME}...")
    
    for root, dirs, files in os.walk(BUILD_DIR):
        # Skip hidden directories like .git, .idea, __pycache__
        if '/.' in root.replace(os.sep, '/'):
            continue
            
        for file in files:
            # Skip build scripts and source files
            if file in ['build.py', 'deploy_to_s3.py', 'site_data.json', 'update_content.py', 'export_data.py', 'README.md', 'AWS_DEPLOYMENT.md', 'requirements.txt']:
                continue
            if file.endswith('.py') or file.endswith('.pyc'):
                continue
            if file.startswith('.'):
                continue
                
            local_path = os.path.join(root, file)
            # relative path in s3
            s3_path = os.path.relpath(local_path, BUILD_DIR).replace(os.sep, '/')
            
            # Mime type
            content_type, _ = mimetypes.guess_type(local_path)
            if content_type is None:
                content_type = 'binary/octet-stream'
            if file.endswith('.css'):
                content_type = 'text/css'
            if file.endswith('.js'):
                content_type = 'application/javascript'
            if file.endswith('.html'):
                content_type = 'text/html'
                
            print(f"Uploading {s3_path} ({content_type})...")
            try:
                s3.upload_file(
                    local_path, 
                    BUCKET_NAME, 
                    s3_path, 
                    ExtraArgs={'ContentType': content_type}
                )
            except Exception as e:
                print(f"Failed to upload {s3_path}: {e}")

    print("Deployment complete!")

if __name__ == "__main__":
    # Check if boto3 is installed
    try:
        import boto3
        deploy()
    except ImportError:
        print("Error: boto3 is not installed. Run 'pip install boto3' first.")
        print("Also ensure you have configured your AWS credentials (aws configure).")
