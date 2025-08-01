import os
import subprocess

# --- IMPORTANT ---
# Make sure this path is EXACTLY where your clang.exe is located.
# Check it in your File Explorer.
clang_path = 'C:/Program Files/LLVM/bin/clang.exe'

print(f"--- Starting Debug ---")
print(f"Testing path: {clang_path}")

# Step 1: Check if the file exists at this path
print(f"Does the file exist? -> {os.path.exists(clang_path)}")

# Step 2: Check if we have execute permissions
# Note: On Windows, this mainly just checks if the path exists.
print(f"Can we execute it? -> {os.access(clang_path, os.X_OK)}")

# Step 3: Try to run the command and capture any error
print("Attempting to run the command...")
try:
    result = subprocess.run(
        [clang_path, '--version'],
        capture_output=True,
        text=True,
        check=True
    )
    print("\n--- SUCCESS! ---")
    print(result.stdout)
except FileNotFoundError:
    print("\n--- ERROR: FileNotFoundError ---")
    print("Python cannot find the file at the specified path. This is the same as [WinError 2].")
    print("Please double-check the 'clang_path' variable for any typos.")
except PermissionError:
    print("\n--- ERROR: PermissionError ---")
    print("Python found the file, but doesn't have permission to run it.")
    print("Try running your terminal 'As Administrator'.")
except Exception as e:
    print(f"\n--- AN UNEXPECTED ERROR OCCURRED ---")
    print(e)

print("\n--- Debug Finished ---")