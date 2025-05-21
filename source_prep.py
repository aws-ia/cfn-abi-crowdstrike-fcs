from pathlib import Path
import sys
import subprocess
import shutil
import os
import tempfile
import zipfile

def package_directory(source_dir: Path, dest_dir: Path) -> None:
    """
    Creates a Lambda deployment package for a directory containing Python files.
    """
    try:
        # Create temporary directory for packages
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Check for requirements.txt
            requirements_file = source_dir / "requirements.txt"
            if requirements_file.exists():
                print(f"Installing requirements for {source_dir.name}...")
                subprocess.run([
                    "pip", "install",
                    "-r", str(requirements_file),
                    "--target", str(temp_path)
                ], check=True)

            # Create zip file
            zip_name = f"lambda.zip"
            zip_path = dest_dir / zip_name

            # Add pip packages to zip
            if os.listdir(temp_path):
                shutil.make_archive(
                    str(zip_path.with_suffix('')),
                    'zip',
                    temp_path
                )
                
                # Add Python files from source directory to existing zip
                with zipfile.ZipFile(zip_path, 'a') as zipf:
                    for file in source_dir.glob('*.py'):
                        zipf.write(file, file.name)
            else:
                # If no requirements, just zip Python files
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for file in source_dir.glob('*.py'):
                        zipf.write(file, file.name)

            print(f"Created package: {zip_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {str(e)}", file=sys.stderr)
    except Exception as e:
        print(f"Error creating package: {str(e)}", file=sys.stderr)

def package_functions(source_path: str, destination_path: str) -> None:
    """
    Creates matching directory structure and packages Python files with dependencies.
    """
    try:
        source = Path(source_path)
        destination = Path(destination_path)

        # Validate source directory exists
        if not source.is_dir():
            raise ValueError(f"Source directory does not exist: {source}")

        # Create destination root if needed
        destination.mkdir(parents=True, exist_ok=True)

        # Mirror directories and create packages
        for dir_path in source.glob('**/'):
            if dir_path.is_dir():
                # Skip __pycache__ and virtual environment directories
                if dir_path.name in ['__pycache__', 'venv', '.env', '.venv']:
                    continue

                # Calculate relative path
                relative_path = dir_path.relative_to(source)
                new_dir = destination / relative_path
                
                # Create new directory
                new_dir.mkdir(parents=True, exist_ok=True)
                print(f"\nProcessing directory: {relative_path}")

                # Package the directory contents if it contains Python files
                if list(dir_path.glob('*.py')):
                    package_directory(dir_path, new_dir)

    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        raise

def copy_templates(source_dir: str, destination_dir: str) -> bool:
    """
    Copy templates directory contents to new source directory.
    """
    try:
        source = Path(source_dir)
        destination = Path(destination_dir)

        # Validate source directory
        if not source.exists():
            raise FileNotFoundError(f"Source directory not found: {source}")

        # Copy directory
        shutil.copytree(source, destination, dirs_exist_ok=True)
        print(f"Successfully copied {source} to {destination}")
        return True

    except Exception as e:
        print(f"Error copying directory: {str(e)}", file=sys.stderr)
        return False

# Example usage
if __name__ == "__main__":
    source_functions = "lambda_functions/source"
    destination_packages = "cfn-abi-crowdstrike-fcs/lambda_functions/packages"
    source_templates = "templates"
    destination_templates = "cfn-abi-crowdstrike-fcs/templates"
    package_functions(source_functions, destination_packages)
    copy_templates(source_templates, destination_templates)