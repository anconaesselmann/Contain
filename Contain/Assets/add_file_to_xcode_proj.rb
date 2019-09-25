#!/usr/bin/env ruby

require 'xcodeproj'

fileDirStrings = ARGV[0]
projectDir = ARGV[1]
projectGroupsString = ARGV[2]

fileDirs = fileDirStrings.split(",")
projectGroups = projectGroupsString.split(",")

xcodeElements = fileDirs.zip(projectGroups)

def add_file_to_group(project, fileDirString, projectGroup)
    changeMade = false
    currentGroup = project.groups[0]

    projectGroup.split("/").each do |groupName|
        groupExists = false
        currentGroup.children.each do |item|
            if item.name == groupName
                currentGroup = item
                groupExists = true
                break
            end
        end
        if not groupExists
            currentGroup = currentGroup.new_group(groupName)
            changeMade = true
        end
    end

    fileExists = false

    fileDir = File.realdirpath(fileDirString)
    currentGroup.children.each do |item|
        if File.realdirpath(item.real_path) == fileDir
            fileExists = true
            break
        end
    end
    if not fileExists
        i = currentGroup.new_file(fileDir)
        project.targets.first.add_file_references([i])
        changeMade = true
    end
    return changeMade
end

project = Xcodeproj::Project.open(projectDir)

projectShouldSave = false
xcodeElements.each do |dir, group|
    if add_file_to_group(project, dir, group)
        projectShouldSave = true
    end
end

if projectShouldSave
    project.save(projectDir)
end

