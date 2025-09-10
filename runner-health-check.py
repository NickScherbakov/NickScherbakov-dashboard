#!/usr/bin/env python3
"""
Health check script for self-hosted runners
Verifies that all required dependencies and environment setup is correct
"""

import sys
import subprocess
import importlib
import platform
import shutil
import os

def check_python_version():
    """Check if Python version is 3.7+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.7+)")
        return False

def check_package(package_name, min_version=None):
    """Check if a Python package is installed"""
    try:
        module = importlib.import_module(package_name)
        if hasattr(module, '__version__'):
            version = module.__version__
            print(f"✅ {package_name} {version}")
        else:
            print(f"✅ {package_name} (installed)")
        return True
    except ImportError:
        print(f"❌ {package_name} (not installed)")
        return False

def check_command(command):
    """Check if a command-line tool is available"""
    if shutil.which(command):
        try:
            result = subprocess.run([command, '--version'], 
                                 capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                print(f"✅ {command}: {version}")
            else:
                print(f"✅ {command} (available)")
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            print(f"✅ {command} (available)")
        return True
    else:
        print(f"❌ {command} (not found)")
        return False

def check_disk_space():
    """Check available disk space"""
    try:
        statvfs = os.statvfs('.')
        free_space = statvfs.f_frsize * statvfs.f_bavail
        free_gb = free_space / (1024**3)
        
        if free_gb >= 10:
            print(f"✅ Disk space: {free_gb:.1f} GB available")
            return True
        else:
            print(f"⚠️  Disk space: {free_gb:.1f} GB available (recommended: 10+ GB)")
            return False
    except (OSError, AttributeError):
        print("❌ Could not check disk space")
        return False

def check_network():
    """Check network connectivity to GitHub"""
    try:
        import urllib.request
        urllib.request.urlopen('https://api.github.com', timeout=10)
        print("✅ Network connectivity to GitHub API")
        return True
    except Exception as e:
        print(f"❌ Network connectivity to GitHub API: {e}")
        return False

def main():
    """Run all health checks"""
    print("🔍 Self-Hosted Runner Health Check")
    print("=" * 40)
    
    checks_passed = 0
    total_checks = 0
    
    # System information
    print(f"\n📋 System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    print(f"   Python executable: {sys.executable}")
    
    # Core requirements
    print(f"\n🐍 Python Environment:")
    total_checks += 1
    if check_python_version():
        checks_passed += 1
    
    # Required packages
    print(f"\n📦 Required Packages:")
    required_packages = ['requests', 'matplotlib', 'seaborn', 'pandas']
    
    for package in required_packages:
        total_checks += 1
        if check_package(package):
            checks_passed += 1
    
    # Command-line tools
    print(f"\n🛠️  Command-line Tools:")
    required_commands = ['git', 'pip']
    
    for command in required_commands:
        total_checks += 1
        if check_command(command):
            checks_passed += 1
    
    # System resources
    print(f"\n💻 System Resources:")
    total_checks += 1
    if check_disk_space():
        checks_passed += 1
    
    # Network connectivity
    print(f"\n🌐 Network:")
    total_checks += 1
    if check_network():
        checks_passed += 1
    
    # Summary
    print(f"\n📊 Health Check Summary:")
    print(f"   Passed: {checks_passed}/{total_checks}")
    
    if checks_passed == total_checks:
        print("🎉 All checks passed! Runner environment is ready.")
        sys.exit(0)
    else:
        print("⚠️  Some checks failed. Please address the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()