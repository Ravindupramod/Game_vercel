
import os
import re
import subprocess
import time

ROOT_DIR = r"d:\Games"
EXCLUDE_DIRS = {".git", "__pycache__", "venv", ".idea", ".vscode", "space_invaders"} # space_invaders already done

def convert_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "import asyncio" in content:
        print(f"Skipping {file_path} (already has asyncio)")
        return False

    print(f"Converting {file_path}...")

    # 1. Add import asyncio
    if "import sys" in content:
        content = content.replace("import sys", "import sys\nimport asyncio")
    else:
        content = "import asyncio\n" + content

    # 2. Async run method
    # Pattern: def run(self):
    content = re.sub(r"def run\(self\):", r"async def run(self):", content)

    # 3. Add await asyncio.sleep(0) in while loop
    # Find 'while running:' and inject await inside
    # We assume 'while running:' is the main loop
    lines = content.splitlines()
    new_lines = []
    in_run_loop = False
    
    for line in lines:
        new_lines.append(line)
        if "while running:" in line:
            # Calculate indentation
            indent = line.split("while")[0]
            # Add sleep with extra indentation
            new_lines.append(f"{indent}    await asyncio.sleep(0)")

    content = "\n".join(new_lines)

    # 4. Refactor main block
    # Check for different main block patterns
    if 'if __name__ == "__main__":' in content:
        # We need to replace the entire block
        # Pattern 1: game = Game(); game.run()
        # Pattern 2: Game().run()
        
        main_block_pattern = r'if __name__ == "__main__":\s+(.*)'
        
        # We will replace the standard block with our async block
        # Using a simpler replace for the common specific patterns found in this codebase
        
        blocks_to_replace = [
            """if __name__ == "__main__":
    game = Game()
    game.run()""",
            """if __name__ == "__main__":
    Game().run()"""
        ]
        
        replacement = """async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())"""

        replaced = False
        for block in blocks_to_replace:
            if block in content:
                content = content.replace(block, replacement)
                replaced = True
                break
        
        if not replaced:
             # Fallback: simple text append if specific pattern match fails, or manual check needed
             # But for now let's try a regex replacement for the end of file
             content = re.sub(r'if __name__ == "__main__":\s+game = Game\(\)\s+game\.run\(\)', replacement, content, flags=re.DOTALL)
             content = re.sub(r'if __name__ == "__main__":\s+Game\(\)\.run\(\)', replacement, content, flags=re.DOTALL)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return True

def build_game(folder_name, file_name):
    # Construct paths
    game_dir = os.path.join(ROOT_DIR, folder_name)
    script_path = os.path.join(game_dir, file_name)
    
    print(f"Building {folder_name}...")
    try:
        # Run pygbag build
        # We use python -m pygbag
        cmd = [sys.executable, "-m", "pygbag", "--build", script_path]
        subprocess.run(cmd, check=True, cwd=ROOT_DIR) # Run from root so paths work like space_invaders
    except subprocess.CalledProcessError as e:
        print(f"Failed to build {folder_name}: {e}")
    except Exception as e:
        print(f"Error building {folder_name}: {e}")

def main():
    import sys
    # Iterate over all directories
    for start_dir in os.listdir(ROOT_DIR):
        full_path = os.path.join(ROOT_DIR, start_dir)
        if not os.path.isdir(full_path):
            continue
        
        if start_dir in EXCLUDE_DIRS:
            continue

        # Look for the main game python file
        # Usually folder ending in _game or just the name
        
        # Assumption: file name matches folder name, or folder_name.py
        expected_script = f"{start_dir}.py"
        script_path = os.path.join(full_path, expected_script)
        
        if not os.path.exists(script_path):
            print(f"Could not find script {expected_script} in {start_dir}")
            continue

        # Convert
        try:
            convert_file(script_path)
            # Build
            # Passing relative path to build_game matching how we did space_invaders
            rel_script_path = os.path.join(start_dir, expected_script)
            
            # Run pygbag command directly here to ensure context
            print(f"Building {rel_script_path}...")
            subprocess.run(["python", "-m", "pygbag", "--build", rel_script_path], cwd=ROOT_DIR, check=False)
            
        except Exception as e:
            print(f"Failed processing {start_dir}: {e}")

if __name__ == "__main__":
    main()
