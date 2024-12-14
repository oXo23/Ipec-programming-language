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
    scrpt_template = ""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input(
            "Enter the path of the .nex file or a file with any file type to compile: "
        )
    with open(filename, "r") as file:
        script = file.read()
    system = os.name
    if system == "nt":
        os.system("cls")
    else:
        os.system("clear")
    path = os.path.dirname(os.path.abspath(__file__))
    scrpt_template += f"cpath = '{path}'\n"
    scrpt_template += f"path = '{filename}'\n"
    script = scrpt_template + script
    log = compile(script)
    cleared = False
    lines = log.split("\n")
    i = 0
    while i < len(lines):
        logl = lines[i]
        if "Traceback" in logl and "Warning" not in logl:
            if not cleared:
                cleared = True
                if system == "nt":
                    os.system("cls")
                else:
                    os.system("clear")
            traceback_lines = lines[i:i+6]
            file_line = traceback_lines[1]
            file_name = file_line.split('"')[1]
            line_num = file_line.split(',')[1].split(' ')[2]
            code_line = script.split("\n")[int(line_num)]
            exception_msg = traceback_lines[4].strip()
            print("!!Traceback!!:")
            print(f"Script: {file_name}")
            print(f"\non line {line_num}:")
            print(f"    {code_line}\n")
            print("Returned:")
            print(f"    {exception_msg}")
            exit(-1)
        i += 1
    os.system("python temp.nexC")
    os.remove("temp.nexC")

if __name__ == "__main__":
    main()
