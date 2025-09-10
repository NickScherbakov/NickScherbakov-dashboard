# Self-Hosted GitHub Actions Runners Setup

This guide explains how to set up and configure self-hosted runners for the NickScherbakov-dashboard repository.

## Overview

Self-hosted runners provide more control over the hardware, operating system, and software tools used in your CI/CD workflows. This repository supports both GitHub-hosted and self-hosted runners.

## Prerequisites

Before setting up a self-hosted runner, ensure you have:

- A machine (physical or virtual) running Linux, macOS, or Windows
- Administrative access to the machine
- Network connectivity to GitHub.com
- Python 3.7 or higher installed
- Git installed

## Runner Requirements

### Hardware Requirements
- **CPU**: 2+ cores recommended
- **RAM**: 4GB+ recommended (8GB+ for better performance)
- **Storage**: 20GB+ free space
- **Network**: Stable internet connection

### Software Requirements
- **Operating System**: Linux (Ubuntu 20.04+ recommended), macOS, or Windows
- **Python**: 3.7+ (3.9+ recommended)
- **Git**: Latest version
- **pip**: Python package installer

### Required Python Packages
The runner will automatically install these packages, but you can pre-install them:
```bash
pip install requests>=2.25.0 matplotlib>=3.3.0 seaborn>=0.11.0 pandas>=1.2.0
```

## Setting Up a Self-Hosted Runner

### Step 1: Navigate to Runner Settings
1. Go to your repository on GitHub
2. Click on **Settings**
3. In the left sidebar, click **Actions** → **Runners**
4. Click **New self-hosted runner**

Or visit directly: https://github.com/NickScherbakov/NickScherbakov-dashboard/settings/actions/runners/new

### Step 2: Choose Your Operating System
Select the appropriate operating system for your runner machine.

### Step 3: Download and Configure
Follow the download and configuration commands provided by GitHub. They will look similar to:

#### For Linux/macOS:
```bash
# Create a folder
mkdir actions-runner && cd actions-runner

# Download the latest runner package
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extract the installer
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Create the runner and start the configuration experience
./config.sh --url https://github.com/NickScherbakov/NickScherbakov-dashboard --token YOUR_TOKEN

# Run it!
./run.sh
```

#### For Windows:
```powershell
# Create a folder under the drive root
mkdir actions-runner; cd actions-runner

# Download the latest runner package
Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-win-x64-2.311.0.zip -OutFile actions-runner-win-x64-2.311.0.zip

# Extract the installer
Add-Type -AssemblyName System.IO.Compression.FileSystem ; [System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD/actions-runner-win-x64-2.311.0.zip", "$PWD")

# Create the runner and start the configuration experience
./config.cmd --url https://github.com/NickScherbakov/NickScherbakov-dashboard --token YOUR_TOKEN

# Run it!
./run.cmd
```

### Step 4: Configure Runner Labels
During configuration, you can add labels to your runner. Recommended labels:
- `self-hosted` (automatically added)
- `dashboard-runner` (for this specific use case)
- Your OS (e.g., `linux`, `macOS`, `windows`)

## Running the Workflow on Self-Hosted Runners

### Option 1: Manual Dispatch
1. Go to **Actions** tab in your repository
2. Select **Update GitHub Profile Dashboard** workflow
3. Click **Run workflow**
4. Choose runner type:
   - `ubuntu-latest` (GitHub-hosted)
   - `self-hosted` (any self-hosted runner)
   - `dashboard-runner` (runners with this specific label)

### Option 2: Default Configuration
By default, scheduled runs and pushes to main will use GitHub-hosted runners (`ubuntu-latest`). To change this default, modify the workflow file.

## Runner Management

### Starting the Runner as a Service

#### Linux (systemd):
```bash
# Install as service
sudo ./svc.sh install

# Start the service
sudo ./svc.sh start

# Check status
sudo ./svc.sh status
```

#### macOS (launchd):
```bash
# Install as service
sudo ./svc.sh install

# Start the service
sudo ./svc.sh start
```

#### Windows (Windows Service):
```powershell
# Run as Administrator
./svc.sh install
./svc.sh start
```

### Monitoring Runner Health
- Check runner status in GitHub repository settings
- Monitor system resources (CPU, memory, disk space)
- Check runner logs for errors
- Ensure network connectivity to GitHub

### Updating the Runner
```bash
# Stop the runner
./svc.sh stop

# Download and extract new version
# (follow download steps above with new version)

# Start the runner
./svc.sh start
```

## Security Considerations

### Network Security
- Ensure the runner machine has secure network configuration
- Use firewalls to restrict unnecessary network access
- Keep the system updated with security patches

### Access Control
- Limit who can add/remove runners
- Use dedicated user accounts for running the service
- Regularly rotate runner tokens
- Monitor runner activity logs

### Secrets Management
- Self-hosted runners have access to repository secrets
- Ensure the runner machine is secure and trusted
- Consider using organization-level runners for better isolation

## Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Install Python 3.9+
sudo apt update
sudo apt install python3 python3-pip  # Ubuntu/Debian
brew install python3  # macOS
```

#### Permission Denied
```bash
# Fix permissions
chmod +x run.sh config.sh
```

#### Network Issues
- Check firewall settings
- Verify GitHub.com connectivity
- Ensure proper DNS resolution

#### Workflow Failures
- Check runner logs: `tail -f _diag/Runner_*.log`
- Verify all dependencies are installed
- Check available disk space and memory

### Getting Help
- Check the runner logs in the `_diag` folder
- Review GitHub Actions documentation
- Contact repository maintainers for specific issues

## Best Practices

1. **Resource Management**: Monitor system resources and scale as needed
2. **Security**: Keep the runner machine secure and updated
3. **Monitoring**: Set up alerts for runner health and workflow failures
4. **Backup**: Regular backups of runner configuration and data
5. **Documentation**: Keep runner setup and configuration documented
6. **Testing**: Test workflows on self-hosted runners before production use

## Workflow Configuration Reference

The workflow supports these runner configurations:
- `ubuntu-latest`: GitHub-hosted Ubuntu runner
- `self-hosted`: Any self-hosted runner
- `dashboard-runner`: Self-hosted runners with the `dashboard-runner` label

You can extend this by modifying `.github/workflows/update-profile.yml` to add more specific runner labels or configurations.