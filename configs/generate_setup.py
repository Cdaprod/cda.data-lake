import os
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

def find_packages(root_dir):
    packages = []
    for root, dirs, files in os.walk(root_dir):
        if "__init__.py" in files:
            package = root.replace(os.path.sep, ".")
            packages.append(package)
    return packages

def generate_setup_py(project_name, version, author, email, description):
    packages = find_packages(project_name)
    setup_content = f"""from setuptools import setup, find_packages

setup(
    name='{project_name}',
    version='{version}',
    author='{author}',
    author_email='{email}',
    description='{description}',
    packages={packages},
    install_requires=[],  # Add dependencies here
    entry_points={{
        'console_scripts': []  # Define console scripts if any
    }},
)
"""
    with open('setup.py', 'w') as f:
        f.write(setup_content)
    print(f"setup.py generated for {project_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate setup.py for a Python project")
    parser.add_argument("--project_name", type=str, default=os.getenv('PROJECT_NAME', 'my_project'))
    parser.add_argument("--version", type=str, default=os.getenv('VERSION', '1.0.0'))
    parser.add_argument("--author", type=str, default=os.getenv('AUTHOR', 'Your Name'))
    parser.add_argument("--email", type=str, default=os.getenv('EMAIL', 'your@email.com'))
    parser.add_argument("--description", type=str, default=os.getenv('DESCRIPTION', 'A short description of the project'))

    args = parser.parse_args()

    generate_setup_py(args.project_name, args.version, args.author, args.email, args.description)
