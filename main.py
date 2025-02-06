# Nex programming language made by @oXo23 on github
# Nex(R) 2023-2024(C)

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

Syntax.extend([
    {"RegEx": r"printJson\((.*?)\)", "To": "print(json.dumps($1))"},
    {"RegEx": r"readFile\((.*?)\)", "To": "with open($1, 'r') as file:\n    return file.read()"},
    {"RegEx": r"writeFile\((.*?), (.*?)\)", "To": "with open($1, 'w') as file:\n    file.write($2)"},
    {"RegEx": r"appendFile\((.*?), (.*?)\)", "To": "with open($1, 'a') as file:\n    file.write($2)"},
    {"RegEx": r"deleteFile\((.*?)\)", "To": "os.remove($1)"},
    {"RegEx": r"listDir\((.*?)\)", "To": "os.listdir($1)"},
    {"RegEx": r"httpGet\((.*?)\)", "To": "requests.get($1).text"},
    {"RegEx": r"httpPost\((.*?), (.*?)\)", "To": "requests.post($1, data=$2).text"},
    {"RegEx": r"jsonParse\((.*?)\)", "To": "json.loads($1)"},
    {"RegEx": r"jsonStringify\((.*?)\)", "To": "json.dumps($1)"},
    {"RegEx": r"sleep\((.*?)\)", "To": "time.sleep($1)"},
    {"RegEx": r"randomInt\((.*?), (.*?)\)", "To": "random.randint($1, $2)"},
    {"RegEx": r"randomFloat\((.*?), (.*?)\)", "To": "random.uniform($1, $2)"},
    {"RegEx": r"currentTime\(\)", "To": "datetime.datetime.now().strftime('%H:%M:%S')"},
    {"RegEx": r"currentDate\(\)", "To": "datetime.datetime.now().strftime('%Y-%m-%d')"},
    {"RegEx": r"formatString\((.*?), (.*?)\)", "To": "$1.format($2)"},
    {"RegEx": r"isEmpty\((.*?)\)", "To": "len($1) == 0"},
    {"RegEx": r"isNull\((.*?)\)", "To": "$1 is None"},
    {"RegEx": r"map\((.*?), (.*?)\)", "To": "list(map($1, $2))"},
    {"RegEx": r"filter\((.*?), (.*?)\)", "To": "list(filter($1, $2))"},
    {"RegEx": r"reduce\((.*?), (.*?)\)", "To": "from functools import reduce\nreduce($1, $2)"},
    {"RegEx": r"unique\((.*?)\)", "To": "list(set($1))"},
    {"RegEx": r"merge\((.*?), (.*?)\)", "To": "$1.update($2)"},
    {"RegEx": r"splitString\((.*?), (.*?)\)", "To": "$1.split($2)"},
    {"RegEx": r"joinList\((.*?), (.*?)\)", "To": "$1.join($2)"},
    {"RegEx": r"contains\((.*?), (.*?)\)", "To": "$1 in $2"},
    {"RegEx": r"length\((.*?)\)", "To": "len($1)"},
    {"RegEx": r"typeOf\((.*?)\)", "To": "type($1).__name__"},
])

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
                    processed_code += [response.text]
                else:
                    raise Exception(f"Failed to fetch {resource}: {response.status_code}")
            else:
                try:
                    with open(resource, "r", encoding="utf-8") as file:
                        processed_code += [file.read()]
                except FileNotFoundError:
                    raise Exception(f"File not found: {resource}")
        else:
            processed_code += [line]
    output_code = "\n".join(processed_code)
    for rule in Syntax:
        output_code = re.sub(
            rule["RegEx"],
            lambda match: re.sub(r'\$(\d+)', lambda m: match.group(int(m.group(1))), rule["To"]),
            output_code
        )

    with open("temp.nexC", "w", encoding="utf-8") as file:
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
    compile(open(filename, "r", encoding="utf-8").read())
    if "-NC" not in sys.argv:
        export("temp.nexC")
    else:
        os.system("python temp.nexC")
        os.remove("temp.nexC")
    return 1  # successful baby!

def export(name):
    # get user system
    system = os.name
    print(sys.argv)
    # get user os, linux = fail,windows=success
    if system == "nt":
        # make a new dir for the compiled app
        app = input("enter app name:")
        print(f'Compiling as "{app}.exe"....\nPlease remember that compiling as a windows executable is still in beta, please report ny issues on github.com/oxo23/nex')
        try:
                os.mkdir(app)
        except FileExistsError as e:
                pass
        except Exception as e:
                raise e
        # converting the nexC file into an .exe
        os.system(f"ren {name} {name.replace(".nexC","")}.py")
        os.system(f"windows.bat {name.replace(".nexC","")}.py")
        # renaming the exe
        os.system(f"ren {name.replace(".nexC","")}.exe {app}.exe")
        # move the exe into the dir
        os.system(f"move {app}.exe {app}")
        # deleting the temp file
        os.remove(f"{name.replace(".nexC","")}.py")
        print(f"Compeleted compiling, your app is at {app}/{app}.exe")
    else:
        print("linux exporting is not supported, use -NC flag next time you run a nex script for ex:python nex.py main.nex -NC")
if __name__ == "__main__":
    main()
