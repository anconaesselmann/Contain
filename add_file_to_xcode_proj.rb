#!/usr/bin/env ruby

require 'xcodeproj'

fileDirString = ARGV[0]
projectDir = ARGV[1]
projectGroup = ARGV[2]

project = Xcodeproj::Project.open(projectDir)

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
        # puts "Creating group " + groupName
        currentGroup = currentGroup.new_group(groupName)
        project.save(projectDir)
    end
end

fileExists = false

fileDir = File.realdirpath(fileDirString)
currentGroup.children.each do |item|
    # puts item.real_path
    if File.realdirpath(item.real_path) == fileDir
        fileExists = true
        break
    end
end
if not fileExists
    # puts "Creating file" + fileDir
    i = currentGroup.new_file(fileDir)
    project.targets.first.add_file_references([i])

    project.save(projectDir)
end
