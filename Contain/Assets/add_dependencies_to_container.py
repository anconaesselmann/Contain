#!/usr/bin/env python

import sys
import os
from glob import glob
import re
import json

from os.path import dirname
from os.path import basename
from os.path import join
from os import path

if len(sys.argv) > 1:
    projectDir = dirname(sys.argv[1])
else:
    print("Error: Project dir has to be passed into " + __file__)


podDir = dirname(__file__)

containerTemplateDir = join(podDir, "Container.template")
dependencyTemplateDir = join(podDir, "Dependency.template")

dependencyInjectionDirName = 'DependencyInjection'

inProjectContainDir = includeDir = join(projectDir, "Contain")
includeDir = join(projectDir, "Contain", "contain.json")
projectName = basename(projectDir)
dependenciesDir = join(projectDir, projectName, dependencyInjectionDirName, 'Dependencies')

xcodeProjDir = join(projectDir, projectName + ".xcodeproj")

if not os.path.exists(dependenciesDir):
    os.makedirs(dependenciesDir)


if not path.exists(includeDir):
    os.makedirs(inProjectContainDir)
    with open(includeDir,"w+") as includeFile:
        includeFile.write("[]")

includeFile = open(includeDir)
jsonArray = json.load(includeFile)
includeFile.close()

containerFileDir = join(projectDir, projectName, dependencyInjectionDirName, 'Container.swift')
consumersFileDir = join(projectDir, projectName, dependencyInjectionDirName, 'Consumers.swift')

if not path.exists(consumersFileDir):
    with open(consumersFileDir,"w+") as consumerFile:
        consumerFile.write("// Create consumer protocols here")

        command = '"' + podDir + '/add_file_to_xcode_proj.rb" "' + consumersFileDir + '" "' + xcodeProjDir + '" "DependencyInjection"'
        os.system(command)

consumersContent = ""
with open(consumersFileDir, 'r') as consuersFile:
    consumersContent = consuersFile.read()

dependenciesFromConsumers = re.findall(r'(?<=protocol\s)([A-Za-z0-9\-_]+)(?:Consumer)', consumersContent)

dependencyTemplate = ""
with open(dependencyTemplateDir, 'r') as dependencyTemplateFile:
    dependencyTemplate = dependencyTemplateFile.read()

for dependency in dependenciesFromConsumers:
    dependencyDir = join(dependenciesDir, dependency + "Dependency.swift")
    if not path.exists(dependencyDir):
        with open(dependencyDir,"w+") as dependencyFile:
            dependencyContent = dependencyTemplate.replace("{class_name}", dependency).replace("{property_name}", dependency[0].lower() + dependency[1:])
            dependencyFile.write(dependencyContent)

# adding file to xcode
for dependency in dependenciesFromConsumers:
    dependencyDir = join(dependenciesDir, dependency + "Dependency.swift")
    command = '"' + podDir + '/add_file_to_xcode_proj.rb" "' + dependencyDir + '" "' + xcodeProjDir + '" "DependencyInjection/Dependencies"'
    os.system(command)

if not path.exists(containerFileDir):
    template = ""
    with open(containerTemplateDir, 'r') as containerTemplateFile:
        template = containerTemplateFile.read()

    dependenciesRequieringImport = list(filter(lambda item: len(item.split(":")) > 1, jsonArray))
    imports = set(map(lambda item: item.split(":")[0], dependenciesRequieringImport))

    importString = "import " + "\nimport ".join(imports) + "\n"

    with open(containerFileDir,"w+") as containerFile:
        containerFile.write(importString + template)

command = '"' + podDir + '/add_file_to_xcode_proj.rb" "' + containerFileDir + '" "' + xcodeProjDir + '" "DependencyInjection"'
os.system(command)

# Todo: add imports for dependencies that were added after container file creation

with open(containerFileDir, 'r') as content_file:
    content = content_file.read()

files = glob(dependenciesDir + "/*.swift")

dependencies = map(lambda item: next(reversed(item.split(":"))) + ".self", jsonArray)
dependencies += map(lambda dir: basename(dir).decode('utf-8').replace('.swift', '.self'), files)

string = ',\n\t\t\t'.encode("utf-8").join(dependencies).encode('ascii','ignore')
content_new = re.sub(r'codeGenDependencyTypes\(\)\s+->\s+\[Dependency\.Type\]\s+\{\s+return(\s+\[\s+[A-Za-z0-9\.,\w\n\s]+?\])', 'codeGenDependencyTypes() -> [Dependency.Type] {\n\t\treturn [\n\t\t\t' + string + "\n\t\t]", content, flags=re.MULTILINE)

with open(containerFileDir,"w+") as containerFile:
    containerFile.write(content_new)
