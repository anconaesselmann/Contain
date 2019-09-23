#!/usr/bin/env python

import sys
import os
from glob import glob
import re
import json

from os.path import dirname
from os.path import basename

if len(sys.argv) > 1:
    projectDir = dirname(sys.argv[1])
else:
    print("Error: Project dir has to be passed into " + __file__)

dependencyInjectionDirName = 'DependencyInjection'

includeDir = os.path.join(projectDir, "Contain", "contain.json")
projectName = basename(projectDir)
dependenciesDir = os.path.join(projectDir, projectName, dependencyInjectionDirName, 'Dependencies')

if not os.path.exists(dependenciesDir):
    os.makedirs(dependenciesDir)

includeFile = open(includeDir)
jsonArray = json.load(includeFile)




containerFile = os.path.join(projectDir, projectName, dependencyInjectionDirName, 'Container.swift')
with open(containerFile, 'r') as content_file:
    content = content_file.read()

files = glob(dependenciesDir + "/*.swift")

dependencies = map(lambda item: next(reversed(item.split(":"))) + ".self", jsonArray)
dependencies += map(lambda dir: basename(dir).decode('utf-8').replace('.swift', '.self'), files)
print(dependencies)

string = ',\n\t\t\t'.encode("utf-8").join(dependencies).encode('ascii','ignore')
content_new = re.sub(r'codeGenDependencyTypes\(\)\s+->\s+\[Dependency\.Type\]\s+\{\s+return(\s+\[\s+[A-Za-z0-9\.,\w\n\s]+?\])', 'codeGenDependencyTypes() -> [Dependency.Type] {\n\t\treturn [\n\t\t\t' + string + "\n\t\t]", content, flags=re.MULTILINE)

f2 = open(containerFile,"w+")
f2.write(content_new)
