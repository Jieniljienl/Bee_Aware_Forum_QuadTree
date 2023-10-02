import subprocess

# Define the list of packages to install
packages_to_install = [
    'flask',
    'flask_sqlalchemy',
    'wtforms',
    'werkzeug',
    # Add other packages to be installed here
]

# Use pip to install each package
for package in packages_to_install:
    subprocess.call(['pip', 'install', package])

print("All packages have been successfully installed")
