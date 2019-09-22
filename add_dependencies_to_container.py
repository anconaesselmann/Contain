#!/usr/bin/env python

import sys
import os
import glob
import re
import json

from os.path import dirname

projectDir = dirname(dirname(os.path.realpath(__file__)))

includeDir = os.path.join(projectDir, "Contain", "contain.json")


includeFile = open(includeDir)
jsonArray = json.load(includeFile)


projectName = sys.argv[1]
dependenciesDir = os.path.join(projectDir, projectName, 'Dependencies')

containerFile = os.path.join(projectDir, projectName, 'Container.swift')
with open(containerFile, 'r') as content_file:
    content = content_file.read()

files = glob.glob(dependenciesDir + "/*.swift")

dependencies = map(lambda item: next(reversed(item.split(":"))) + ".self", jsonArray)
dependencies += map(lambda dir: os.path.basename(dir).decode('utf-8').replace('.swift', '.self'), files)
# print(dependencies)

string = ',\n\t\t\t'.encode("utf-8").join(dependencies).encode('ascii','ignore')
content_new = re.sub(r'codeGenDependencyTypes\(\)\s+->\s+\[Dependency\.Type\]\s+\{\s+return(\s+\[\s+[A-Za-z0-9\.,\w\n\s]+?\])', 'codeGenDependencyTypes() -> [Dependency.Type] {\n\t\treturn [\n\t\t\t' + string + "\n\t\t]", content, flags=re.MULTILINE)

f2 = open(containerFile,"w+")
f2.write(content_new)
