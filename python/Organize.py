import os
import time
from enum import Enum
import FileInfo

class SortMethod(Enum):
    ALPHABETICAL = 0
    EXTENSION = 1
    DATE = 2
    TAG = 3

# Isolates file name from any path still possibly attached
def IsolateFile(filePath):
    i = filePath.rfind(os.sep)
    if i != -1:
        return filePath[i + 1:]
    else:
        return filePath

def MoveFile(originalLocation, targetLocation, folderName, file):
    os.makedirs(os.path.join(targetLocation, folderName), exist_ok=True)
    newLocation = os.path.join(targetLocation, folderName, IsolateFile(file))
    os.rename(os.path.join(originalLocation, file), newLocation)

def AddFolderFiles(directory, originalDirectoryLength):
    files = os.listdir(directory)
    newFiles = []
    for file in files:
        filePath = os.path.join(directory, file)
        if os.path.isdir(filePath):
            newFiles += AddFolderFiles(filePath, originalDirectoryLength)
        elif os.path.isfile(filePath):
            newFiles.append(filePath[(originalDirectoryLength + 1):])

    return newFiles

def SortFiles(directory, target, method, includingFolders, allLetters=False, letterRanges=None, usingGroups=False, usingCustomGroups=False, fileGroups=None, nameTag=None, tagFolder=None):
    if includingFolders:
        fileList = AddFolderFiles(directory, len(directory))
    else:
        fileList = os.listdir(directory)
    for file in fileList:
        if not os.path.isfile(os.path.join(directory, file)):
            continue
        match method:

            # Alphabetical sorting
            case SortMethod.ALPHABETICAL:
                if allLetters:
                    if IsolateFile(file)[0].isalpha():
                        MoveFile(directory, target, IsolateFile(file)[0].upper(), file)
                    else:
                        MoveFile(directory, target, "Misc", file)
                else:
                    tempFile = IsolateFile(file)
                    targetRange = ""
                    for letterRange in letterRanges:
                        if not file[0].isalpha():
                            break
                        if (len(letterRange) == 1 and tempFile[0].upper() == letterRange) or (len(letterRange) != 1 and (
                                ord(letterRange[0].upper()) <= ord(tempFile[0].upper()) <= ord(letterRange[2].upper()))):
                            targetRange = letterRange
                            break
                    if targetRange == "":
                        MoveFile(directory, target, "Misc", file)
                    else:
                        MoveFile(directory, target, targetRange, file)

            # File extension sorting
            case SortMethod.EXTENSION:
                splitFile = file.split('.')
                extension = '.' + splitFile[len(splitFile) - 1].lower()
                if not usingGroups:
                    MoveFile(directory, target, extension, file)
                else:
                    if usingCustomGroups:
                        foundGroup = False
                        for group in fileGroups:
                            groupName = ', '.join(group)
                            if extension in group:
                                MoveFile(directory, target, groupName, file)
                                foundGroup = True
                                break
                        if not foundGroup:
                            MoveFile(directory, target, extension, file)

                    else:
                        definition = FileInfo.GetDefinition(extension)
                        MoveFile(directory, target, definition, file)

            # File date sorting
            case SortMethod.DATE:
                months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
                fileTime = time.localtime(os.path.getctime(os.path.join(directory, file)))
                if usingGroups:
                    MoveFile(directory, target, f"{months[fileTime.tm_mon - 1]} {fileTime.tm_year}", file)
                else:
                    MoveFile(directory, target, f"{fileTime.tm_year}", file)

            # Sorting files with a certain tag in their name
            case SortMethod.TAG:
                isolatedFile = IsolateFile(file)
                extensionStart = isolatedFile.rfind('.')
                isolatedFile = isolatedFile[0:extensionStart]
                if nameTag.lower() in isolatedFile.lower():
                    if not tagFolder:
                        MoveFile(directory, target, nameTag, file)
                    else:
                        MoveFile(directory, target, tagFolder, file)


    print("Done!")

def CheckLetterRange(ranges):
    ranges = ranges.replace(" ", "")
    rangeList = ranges.split(',')
    letterCount = len(rangeList)
    for lRange in rangeList:
        if len(lRange) != 3:
            return False
        if not (lRange[2].isalpha and lRange[0].isalpha):
            return False
        letterCount += (ord(lRange[2].upper()) - ord(lRange[0].upper()))
    return letterCount == 26

def Start():
    directoryToOrganize = input("Directory to organize: ")
    while not os.path.exists(directoryToOrganize):
        directoryToOrganize = input("The directory to organize you entered does not exist. Please enter it again: ")
    targetDirectory = directoryToOrganize
    samePlaceInput = input("Put folders in same directory? (Y/N): ")
    if samePlaceInput.upper() != 'Y':
        targetDirectory = input("Target directory: ")
        while not os.path.exists(targetDirectory):
            targetDirectory = input("The target directory to put the organized files in does not exist. Please try again: ")
    foldersInput = input("Include files already inside folders? (Y/N): ")
    includeFolders = False
    if foldersInput.upper() == 'Y': includeFolders = True

    print("How will the files be organized?\n1. Alphabetical\n2. File Extension/Type\n3. Date Created\n4. Tags within file names\n")
    userChoice = input('> ')
    match userChoice:

        case '1':
            allLettersInput = input("Will you be sorting every letter individually? (Y/N): ")
            if allLettersInput.lower() == 'y':
                SortFiles(directoryToOrganize, targetDirectory, SortMethod.ALPHABETICAL, includeFolders, allLetters=True)
            else:
                rangeInput = input("Enter specific letter ranges to sort by (Example: A-D, E-F, G-Z): ")
                while not CheckLetterRange(rangeInput):
                    rangeInput = input("Invalid Range. Please try again: ")
                rangeInput = rangeInput.replace(" ", "")
                rangeList = rangeInput.split(',')
                SortFiles(directoryToOrganize, targetDirectory, SortMethod.ALPHABETICAL, includeFolders, letterRanges=rangeList)

        case '2':
            filesGrouped = input("Would you like certain file types to be grouped together? (Y/N): ")
            if filesGrouped.upper() == 'Y':
                customNames = input("Use built-in (Documents, Videos, Images, etc)? (Y/N): ")
                if customNames.upper() == 'Y':
                    SortFiles(directoryToOrganize, targetDirectory, SortMethod.EXTENSION, includeFolders, usingGroups=True, usingCustomGroups=False)
                else:
                    fileGroups = []
                    while True:
                        group = input("Add file types to be grouped, separated by commas (.pdf, .txt, .docx). Enter nothing to finish: ")
                        if not group:
                            break
                        group = group.replace(' ', '').split(',')
                        fileGroups.append(group)
                    SortFiles(directoryToOrganize, targetDirectory, SortMethod.EXTENSION, includeFolders, usingGroups=True, usingCustomGroups=True, fileGroups=fileGroups)
            else:
                SortFiles(directoryToOrganize, targetDirectory, SortMethod.EXTENSION, includeFolders)

        case '3':
            dateSortChoice = input("Would you like to sort by month or year? (MONTH/YEAR): ").lower()
            while dateSortChoice != ("month" or "year"): dateSortChoice = input("Try again (MONTH/YEAR): ").lower()
            if dateSortChoice == "month":
                SortFiles(directoryToOrganize, targetDirectory, SortMethod.DATE, includeFolders, usingGroups=True)
            else:
                SortFiles(directoryToOrganize, targetDirectory, SortMethod.DATE, includeFolders, usingGroups=False)

        case '4':
            tag = input("Include files with what in their file name? (Example: *HIST 1101* Essay 1): ")
            folderName = input("What should the folder be called? (Leave blank to use tag given): ")
            SortFiles(directoryToOrganize, targetDirectory, SortMethod.TAG, includeFolders, nameTag=tag, tagFolder=folderName)

        case _:
            print("Invalid choice.")