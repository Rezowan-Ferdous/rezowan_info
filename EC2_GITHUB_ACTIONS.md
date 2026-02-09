# Hosting on EC2 with Automated GitHub Actions

This guide explains how to set up an EC2 instance to serve your static site and configure GitHub Actions to deploy changes automatically.

## Part 1: Configure Your EC2 Instance (Manual Setup - Do Once)

1.  **Launch Instance**:
    *   **OS**: Ubuntu 22.04 LTS (recommended).
    *   **Size**: `t2.micro` (free tier).
    *   **Key Pair**: Download the `.pem` file.
    *   **Security Group**: Allow **SSH (22)**, **HTTP (80)**, **HTTPS (443)**.

2.  **Connect to EC2**:
    From your local terminal:
    ```bash
    ssh -i /path/to/key.pem ubuntu@your-ec2-ip
    ```

3.  **Install Software**:
    *   **For Ubuntu**:
        ```bash
        sudo apt update
        sudo apt install nginx git python3-pip -y
        ```
    *   **For Amazon Linux 2023 (ec2-user)**:
        ```bash
        sudo dnf update -y
        sudo dnf install git nginx python3-pip -y
        sudo systemctl start nginx
        sudo systemctl enable nginx
        ```
    *   **For Amazon Linux 2 (legacy)**:
        ```bash
        sudo amazon-linux-extras install nginx1 -y
        sudo systemctl start nginx
        sudo systemctl enable nginx
        ```

4.  **Clone Your Repo**:
    ```bash
    cd ~
    git clone https://github.com/Rezowan-Ferdous/rezowan_info.git
    cd rezowan_info
    pip3 install -r requirements.txt
    python3 build.py
    ```

6.  **Configure Nginx (Amazon Linux)**:
    Since I've created an `nginx.conf` in the repo for you, just copy it:
    ```bash
    # Backup original
    sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
    
    # Overwrite with ours
    sudo cp /home/ec2-user/rezowan_info/nginx.conf /etc/nginx/nginx.conf
    
    # Fix permissions so Nginx can read your files
    chmod 711 /home/ec2-user
    chmod 755 /home/ec2-user/rezowan_info
    
    # Restart Nginx
    sudo systemctl restart nginx
    ```

    **Important Troubleshooting**:
    *   **Check Status**: `sudo systemctl status nginx` (should be Active: active (running)).
    *   **Check Firewall (Security Group)**: Go to AWS Console > EC2 > Instances > (Select Instance) > Security > Security Groups. Ensure there is an Inbound Rule allowing **Type: HTTP, Port: 80, Source: 0.0.0.0/0**. If this is missing, the site won't load even if Nginx is running.

---

## Part 2: Automate with GitHub Actions

To make the site update automatically when you push code:

1.  **Get Your SSH Key**:
    *   Open your downloaded `.pem` key file in a text editor.
    *   Copy the *entire* content (including `-----BEGIN RSA PRIVATE KEY-----`).

2.  **Add Secrets to GitHub**:
    *   Go to your Repo > **Settings** > **Secrets and variables** > **Actions**.
    *   Add **New Repository Secret**:
        *   `EC2_HOST`: Your EC2 IP address (e.g., `1.2.3.4`).
        *   `EC2_USER`: `ubuntu`.
        *   `EC2_SSH_KEY`: Paste your key content.

3.  **The Workflow File**:
    This file is automatically created at `.github/workflows/deploy.yml`. It tells GitHub to SSH into your server, pull the code, and rebuild the site.

---

---

## Part 3: Connect Domain & Enable HTTPS (SSL)

### 1. Point Your Domain (DNS)
1.  Go to your Domain Registrar (Route 53, GoDaddy, Namecheap, etc.).
2.  Create an **A Record**.
    *   **Name**: `@` (root) and `www`.
    *   **Value**: Your EC2 Public IP (`34.228.36.92`).
3.  Wait a few minutes for DNS to propagate.

### 2. Enable HTTPS (Free SSL with Certbot)
SSH into your EC2 and run these commands to install Certbot and automatically configure Nginx.

**For Amazon Linux 2023**:
```bash
# 1. Install Certbot and the Nginx plugin
sudo dnf install python3-certbot-nginx -y

# 2. Run Certbot (Follow the prompts!)
sudo certbot --nginx
```

**For Amazon Linux 2**:
```bash
sudo amazon-linux-extras install epel -y
sudo yum install certbot python-certbot-nginx -y
sudo certbot --nginx
```

**During Certbot setup**:
1.  Enter your email (for urgent renewal notices).
2.  Agreet to Terms (`Y`).
3.  **Enter your domain name(s)** (e.g., `rezowan.com www.rezowan.com`).
4.  Certbot will verify the domain points to this server.
5.  It will ask to redirect HTTP to HTTPS -> Choose **2** (Redirect).

**Auto-Renewal**:
Certbot certificates last 90 days. Test auto-renewal:
```bash
sudo certbot renew --dry-run
```
If that works, you are set forever!

---

## Troubleshooting "404 Not Found"
If you see a "404 Not Found" nginx page:

1.  **Check if `index.html` exists**:
    ```bash
    ls -l /home/ec2-user/rezowan_info/index.html
    ```
    *   **If missing**: Run `python3 build.py` inside the folder.
    *   **If present**: Check permissions.

2.  **Check Nginx Config**:
    Ensure `root` points to the right place.
    ```bash
    cat /etc/nginx/nginx.conf | grep root
    # Should say: root /home/ec2-user/rezowan_info;
    ```

3.  **Conflicting Configs**:
    Sometimes a default config file interferes.
    ```bash
    ls /etc/nginx/conf.d/
    # If you see default.conf, rename it:
    sudo mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.disabled
    sudo systemctl restart nginx
    ```

