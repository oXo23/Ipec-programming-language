# nmm (Nex Module Manager)
# get args
import sys
import os
import requests

args = sys.argv
libs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libs")

if len(args) < 2:
    print("Usage: nmm <command> [args]")
    print("Use nmm -h for help")
    exit(1)

# get command
if args[1] == "-h":
  print("Usage: nmm <command> [args]")
  print("Use nmm -h for help and to print this message.\n")
  print("Commands:")
  print("-i <url> <as> - Installs a module from the given url and save it as the <as> argument.")
  print("-del <module> - Deletes a module from the given name.")
  print("-ls - Lists all installed modules.")
  print("-h - Prints this message.")
  exit(0)

if args[1] == "-i":
  if len(args) < 4:
    print("Usage: nmm -i <url> <as>")
    exit(1)
  url = args[2]
  as_ = args[3]
  if not url.startswith("http://") and not url.startswith("https://"):
    print("Invalid url")
    exit(1)
  if not as_.endswith(".nex"):
    print("Invalid file extension for <as> argument.")
    exit(1)
  # make the libs path if it doesn't exist
  if not os.path.exists(libs_path):
    os.makedirs(libs_path)
  # download the module
  r = requests.get(url)
  if r.status_code != 200:
    print("Failed to download module.")
    exit(1)
  # save the module
  with open(os.path.join(libs_path, as_), "w") as f:
    f.write(r.text)
  print("Module installed successfully.")
  exit(0)

if args[1] == "-del":
  if len(args) < 3:
    print("Usage: nmm -del <module>")
    exit(1)
  module = args[2]
  if not os.path.exists(os.path.join(libs_path, module)):
    print("Module not found.")
    exit(1)
  os.remove(os.path.join(libs_path, module))
  print("Module deleted successfully.")
  exit(0)

if args[1] == "-ls":
  if not os.path.exists(libs_path):
    print("No modules installed.")
    exit(0)
  print("Installed modules:")
  for module in os.listdir(libs_path):
    if module.endswith(".nex"):
      print(module)
  exit(0)

print("Invalid command.")
print("use nmm -h for help!")