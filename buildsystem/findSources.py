#!/usr/bin/python3
import pathlib
import argparse

def findFilesByExtension(path, extensions):
    files = []
    if path.is_dir():
        for path in path.iterdir():
            if path.is_file():
                if extensions == None:
                    files.append(str(path))
                else:
                    for extension in extensions:
                        if (extension == path.suffix):
                            files.append(str(path))
            elif path.is_dir():
                files.extend(findFilesByExtension(path, extensions))
    else:
        print("findFilesByExtension: Not a directory: " + path)

    return files

def toCMakeList(listName, list):
    list.insert(0, listName)
    list.insert(0, "set(")
    list.append(")")

    return ' '.join(list)



parser = argparse.ArgumentParser(description="A build tool")

parser.add_argument("-l", "--list-name", action="store", required=True)
parser.add_argument("-e", "--with-extension", action="append", metavar="EXTENSION")
parser.add_argument("-o", "--output", action="store")
parser.add_argument("folders", action="store", nargs="+")

args = parser.parse_args()

print(args.list_name)
print(args.with_extension)
print(args.folders)
print(args.output)

for folder in args.folders:
    path = pathlib.Path(folder)
    if not (path.exists() and path.is_dir()):
        print("Invalid folder: " + folder)
        exit(1)

files = []
for folder in args.folders:
    path = pathlib.Path(folder)
    files.extend(findFilesByExtension(path, args.with_extension))

cmakeList = toCMakeList(args.list_name, files)
if not args.output:
    print(cmakeList)
else:
    with open(args.output, "w") as file:
        file.write(cmakeList)