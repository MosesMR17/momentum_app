import os

def check_project_state():
    print("=== PROJECT STRUCTURE DIAGNOSTIC ===")
    print(f"Current Working Directory: {os.getcwd()}")
    print("\nProject Files Found:")
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden or environment folders to keep it clean
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', '.venv', '.idea']]
        for file in files:
            if file.endswith(('.py', '.txt', '.json', '.md', '.csv', '.html')):
                rel_path = os.path.relpath(os.path.join(root, file), '.')
                print(f"  [File] {rel_path}")

if __name__ == "__main__":
    check_project_state()
    