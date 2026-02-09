# AWS Static Site Deployment Guide

This guide details how to host your static website on AWS using **S3** (storage), **CloudFront** (CDN/HTTPS), and **Route 53** (DNS).

## Prerequisites
- AWS Account
- Registered Domain Name
- Generated static files (run `python build.py`)

## Step 1: Create an S3 Bucket
1.  Login to **AWS Console** > **S3**.
2.  Click **Create bucket**.
3.  **Bucket name**: `your-domain-name.com` (e.g., `rezowan.com`).
4.  **Region**: Choose one close to your users (e.g., `us-east-1` or `eu-west-2`).
5.  **Object Ownership**: ACLs disabled (recommended).
6.  **Block Public Access**: **Uncheck** "Block all public access" (we need it public for the website, or restricted via CloudFront).
    *   *Secure Option*: Keep Block Public Access **ON** and use a CloudFront Origin Access Control (OAC). This is recommended.
7.  Click **Create bucket**.

## Step 2: Upload Files (Initial Test)
1.  Go into your new bucket.
2.  Click **Upload**.
3.  Drag and drop the contents of your `build` output folder (specifically `index.html`, etc.).
    *   **Important**: Do NOT upload the root folder itself, upload the *contents* (`index.html`, `research.html`, `static/`, etc.).
4.  Click **Upload**.

## Step 3: Request SSL Certificate (ACM)
1.  Go to **AWS Certificate Manager (ACM)**.
2.  **Region**: You **MUST** switch to **US East (N. Virginia) us-east-1** (required for CloudFront).
3.  Click **Request certificate** > **Request a public certificate**.
4.  **Domain names**: Add `your-domain.com` and `*.your-domain.com`.
5.  **Validation method**: DNS validation.
6.  Click **Request**.
7.  Click on the certificate ID.
8.  Click **Create records in Route 53** if you use Route 53, or copy the CNAME records to your other DNS provider.
9.  Wait for status to change to **Issued**.

## Step 4: Create CloudFront Distribution
1.  Go to **CloudFront**.
2.  Click **Create distribution**.
3.  **Origin domain**: Select your S3 bucket.
4.  **Origin access**: Choose **Origin access control settings (recommended)**.
    *   Click **Create control setting** > Create.
    *   (You will need to update S3 bucket policy later).
5.  **Viewer protocol policy**: Redirect HTTP to HTTPS.
6.  **Alternate domain name (CNAME)**: Enter `your-domain.com` and `www.your-domain.com`.
7.  **Custom SSL certificate**: Select the ACM certificate you created in Step 3.
8.  **Default root object**: `index.html`.
9.  Click **Create distribution**.
10. **IMPORTANT**: You will see a banner "The S3 bucket policy needs to be updated". Click **Copy policy**.
11. Go back to your **S3 Bucket** > **Permissions** tab > **Bucket policy** > **Edit** > Paste the policy > **Save**.

## Step 5: specific Configuration for Subdirectories (Routing)
Since your site uses folders like `/research/` implies `/research/index.html`, CloudFront/S3 basic setup works for `index.html` but specific subpaths might need a CloudFront Function if you want clean URLs (e.g. `rezowan.com/research` instead of `rezowan.com/research/index.html`).
*   *Note*: Your current `build.py` generates `index.html` inside folders, so `rezowan.com/research/` should work automatically if S3 Static Website Hosting is used.
*   **Alternative for Clean URLs**:
    *   If using S3 Static Website Endpoint as Origin: It handles `index.html` automatically.
    *   If using S3 Bucket directly (OAC): You need a CloudFront Function to rewrite URLs.

**Simple Path (S3 Website Endpoint)**:
1.  In S3 Bucket > Properties > **Static website hosting** > Enable.
2.  Index document: `index.html`.
3.  In CloudFront, change Origin Domain to the **S3 Website Endpoint** (it looks like `http://bucket-name.s3-website-region.amazonaws.com`), NOT the bucket selection dropdown.

## Step 6: Point Domain to CloudFront
1.  Go to **Route 53** (or your DNS provider).
2.  Create Record (A Record).
3.  Toggle **Alias**.
4.  Choose **Alias to CloudFront distribution**.
5.  Select your distribution.
6.  Save.

---

## Alternative: Hosting on EC2 (Advanced)
If you prefer using an EC2 instance (e.g., if you plan to add dynamic backend logic later or already have a server), follow this:

1.  **Launch Instance**: Amazon Linux 2 or Ubuntu.
2.  **Security Group**: Allow HTTP (80) and HTTPS (443).
3.  **Connect (SSH)** to your instance.
4.  **Install Nginx**:
    ```bash
    sudo yum update -y
    sudo yum install nginx -y
    sudo systemctl start nginx
    sudo systemctl enable nginx
    ```
5.  **Clone Your Repo**:
    ```bash
    sudo yum install git -y
    git clone https://github.com/YourUsername/rezowan_info.git
    cd rezowan_info
    ```
6.  **Build**:
    You'll need Python on the EC2 to run the build script.
    ```bash
    pip3 install -r requirements.txt
    python3 build.py
    ```
7.  **Configure Nginx**:
    Point Nginx root to your build output.
    ```bash
    sudo nano /etc/nginx/nginx.conf
    # Change 'root' to /home/ec2-user/rezowan_info
    ```
8.  **Restart Nginx**: `sudo systemctl restart nginx`

**S3 vs EC2 for Static Sites**:
- **S3 + CloudFront**: Cheaper, faster (CDN), zero maintenance, no patching. **Recommended**.
- **EC2**: Full control, but requires OS updates, security patches, and manual scaling.

**Q: Can I "pull" my repo in S3?**
No, S3 is just file storage. It cannot run `git` commands.
- **Solution**: Use **GitHub Actions** to automatically build and upload to S3 whenever you push to GitHub.

