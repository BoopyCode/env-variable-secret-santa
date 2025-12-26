#!/usr/bin/env python3
"""Env Variable Secret Santa - Because .env files shouldn't play hide-and-seek with your sanity."""

import os
import sys
import re
from pathlib import Path

def find_env_files():
    """Scans for .env files like a detective looking for clues at a crime scene."""
    env_files = []
    for root, _, files in os.walk('.'):
        for file in files:
            if file.startswith('.env'):
                env_files.append(Path(root) / file)
    return env_files

def check_env_file(env_path):
    """Checks if your .env file is naughty or nice."""
    try:
        content = env_path.read_text()
        
        # Look for secrets that shouldn't be here (like Santa checking his list)
        secrets = re.findall(r'(?i)(password|secret|key|token)\s*=\s*[\"\']?[^\s\"\']+', content)
        
        if secrets:
            print(f"🎅 HO HO NO! {env_path} contains potential secrets:")
            for secret in secrets[:3]:  # Show first 3 to avoid spoilers
                print(f"   - {secret.split('=')[0].strip()}")
            if len(secrets) > 3:
                print(f"   ... and {len(secrets) - 3} more naughty variables")
            return False
        
        # Check if it's just an example file
        if '.example' in env_path.name or '.sample' in env_path.name:
            print(f"✓ {env_path} - Example file (nice!)")
        else:
            print(f"✓ {env_path} - Looks clean (you get a cookie!)")
        return True
        
    except Exception as e:
        print(f"❌ {env_path} - Error reading: {e}")
        return False

def main():
    """The main sleigh ride."""
    print("\n🎄 Env Variable Secret Santa is checking your list...\n")
    
    env_files = find_env_files()
    
    if not env_files:
        print("No .env files found. Did you forget to invite Santa?")
        return
    
    naughty_files = 0
    for env_file in env_files:
        if not check_env_file(env_file):
            naughty_files += 1
    
    print(f"\n🎁 Summary: {len(env_files) - naughty_files} nice files, {naughty_files} naughty files")
    
    if naughty_files > 0:
        print("\n⚠️  Warning: Some files might contain secrets. Check before committing!")
        sys.exit(1)
    else:
        print("\n🎉 All files are ready for the version control party!")

if __name__ == "__main__":
    main()
