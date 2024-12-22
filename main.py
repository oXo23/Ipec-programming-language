# Nex programming language made by @oXo23 on github
# Nex(R) 2023-2024(C)

# exporting config
exports = {
    "windows":"windows.bat $1 $2",
    # linux:"bash linux.sh $1 $2", coming soon
}

import re
import subprocess
import sys
import os
import requests

Syntax = [
    # log
    {"RegEx": r"log\((.*?)\)", "To":"print($1)"},
    # if
    {"RegEx":"if (.*?) then", "To":"if $1:"},
    # else
    {"RegEx":"else", "To":"else:"},
    # elif
    {"RegEx":"elif (.*?) then", "To":"elif $1:"},
    # putPy
    {"RegEx":"putPy (.*?)", "To":"import $1"},
    # evalPy
    {"RegEx":"evalPy(.*?)", "To":"eval($1)"},
    # for
    {"RegEx": "for (.*?) do", "To":"for $1:"},
    # while
    {"RegEx": "while (.*?) do", "To":"while $1:"},
    # func
    {"RegEx": "func (.*?) do", "To":"def $1:"},
    # class
    {"RegEx": "class (.*?) do", "To":"class $1:"},
    # try
    {"RegEx": "try (.*?) do", "To":"try $1:"},
    # except
    {"RegEx": "except (.*?) do", "To":"except $1:"},
    # finally
    {"RegEx": "finally (.*?) do", "To":"finally $1:"},
    # end
    {"RegEx": "end", "To":"pass"},
    # break
    {"RegEx": "break", "To":"break"},
    # continue
    {"RegEx": "continue", "To":"continue"},
    # return
    {"RegEx": "ret (.*?)", "To":"return $1"},
    # var
    {"RegEx": "(.*) = (.*?)", "To":"$1 = $2"},
    # global
    {"RegEx": "global (.*?)", "To":"global $1"},
    # @
    {"RegEx": "@(.*?)", "To":"@$1"},
    # del
    {"RegEx": "del (.*?)", "To":"del $1"},
    # quit
    {"RegEx": r"quit\((.*?)\)", "To":"exit($1)"},
    # throw
    {"RegEx": "throw (.*?)", "To":"raise $1"}
]


def compile(source_code):
    global log
    log = ""
    output_code = source_code.splitlines()
    processed_code = []
    for line in output_code:
        if line.startswith("put "):
            resource = line[4:].strip()
            if resource.startswith("http://") or resource.startswith("https://"):
                response = requests.get(resource)
                if response.status_code == 200:
                    processed_code.append(response.text)
                else:
                    raise Exception(f"Failed to fetch {resource}: {response.status_code}")
            else:
                try:
                    with open(resource, "r") as file:
                        processed_code.append(file.read())
                except FileNotFoundError:
                    raise Exception(f"File not found: {resource}")
        else:
            processed_code.append(line)
    output_code = "\n".join(processed_code)
    for rule in Syntax:
        output_code = re.sub(
            rule["RegEx"],
            lambda match: re.sub(r'\$(\d+)', lambda m: match.group(int(m.group(1))), rule["To"]),
            output_code)


    with open("temp.nexC", "w") as file:
        file.write(output_code)
    process = subprocess.Popen(
        ["python", "temp.nexC"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    log = stdout + stderr
    return log


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "-NC":
        filename = sys.argv[1]
    else:
        filename = input(
            "Enter the path of the .nex file or a file with any file type to compile: "
        )
    system = os.name
    if system == "nt":
        os.system("cls")
    else:
        os.system("clear")
    compile(open(filename, "r").read())
    # compile if no -NC flag was not given
    if "-NC" not in sys.argv:
        print('Compiling as "compiled.exe"....\nPlease remember that compiling as a windows executable is still in beta, please report ny issues on github.com/oxo23/nex')
        export("temp.nexC")
    else:
        os.system("python temp.nexC")
        os.remove("temp.nexC")
    return 1 # succesful baby!

def export(name):
    # get user system
    system = os.name
    print(sys.argv)
    # get user os, linux = fail,windows=success
    if system == "nt":
        # make a new dir for the compiled app
        app = input("enter app name:")
        os.mkdir(app)
        os.system(exports["windows"].replace("$1", "temp_win.bat").replace("$2", f"../{app}/compiled.exe"))
        # copy the nex script into the dir as main.py
        os.system(f"copy {name} {app}/bin/main.py")
    else:
        print("linux exporting is not supported, use -NC flag next time you run a nex script for ex:nex.py main.nex -NC")
if __name__ == "__main__":
    res = main()
    del res # res ain't used for anything anyways
