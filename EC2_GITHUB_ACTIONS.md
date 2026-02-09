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
    ```bash
    sudo apt update
    sudo apt install nginx git python3-pip -y
    ```

4.  **Clone Your Repo**:
    ```bash
    cd ~
    git clone https://github.com/Rezowan-Ferdous/rezowan_info.git
    cd rezowan_info
    pip3 install -r requirements.txt
    python3 build.py
    ```

5.  **Configure Nginx**:
    Point Nginx to your repo folder.
    ```bash
    sudo nano /etc/nginx/sites-available/default
    # Change 'root /var/www/html;' to 'root /home/ubuntu/rezowan_info;'
    # Save (Ctrl+O, Enter, Ctrl+X)
    sudo systemctl restart nginx
    ```
    Your site should now be live on your EC2 IP.

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

## Troubleshooting
*   **Permission Denied**: Check that your `.pem` key permissions are correct (`chmod 400 key.pem`).
*   **Git Pull Failed**: If using a private repo, you may need to add an SSH key to GitHub for the EC2 user.
