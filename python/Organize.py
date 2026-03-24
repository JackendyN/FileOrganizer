import os

def SortFile(originalLocation, targetLocation, folderName, file):
    os.makedirs(os.path.join(targetLocation, folderName), exist_ok=True)
    newLocation = os.path.join(targetLocation, folderName, file)
    os.rename(os.path.join(originalLocation, file), newLocation)

def GetDefinition(extension, definitions):
    for definition, extensions in definitions.items():
        if extension in extensions:
            return definition
    return "Other"

def AlphabeticalSort(directory, target, sortingAll, allLetters, letterRanges=None):
    fileList = os.listdir(directory)
    for file in fileList:
        if os.path.isfile(os.path.join(directory, file)):
            if allLetters:
                if file[0].isalpha():
                    SortFile(directory, target, file[0].upper(), file)
                else:
                    SortFile(directory, target, "Misc", file)
            else:
                targetRange = ""
                for letterRange in letterRanges:
                    if not file[0].isalpha():
                        break
                    if (len(letterRange) == 1 and file[0].upper() == letterRange) or (len(letterRange) != 1 and (ord(letterRange[0].upper()) <= ord(file[0].upper()) <= ord(letterRange[2].upper()))):
                        targetRange = letterRange
                        break
                if targetRange == "":
                    if sortingAll:
                        SortFile(directory, target, "Misc", file)
                    else:
                        continue
                else:
                    SortFile(directory, target, targetRange, file)

    print("Done!")

def FileTypeSort(directory, target, sortingAll, usingGroups, usingCustomGroups, fileGroups = None):
    fileDefinitions = { # Revised with AI
        "Documents": {
        ".doc", ".docx", ".pdf", ".txt", ".rtf",
        ".odt", ".pages", ".md"
        },
        "Spreadsheets": { ".xls", ".xlsx", ".csv", ".ods" },
        "Presentations": { ".ppt", ".pptx", ".key" },
        "Source Code": {
            ".py", ".java", ".cs", ".cpp", ".c", ".h",
            ".js", ".ts", ".html", ".css", ".php",
            ".rb", ".go", ".swift", ".kt", ".sql"
        },
        "Images": {
            ".png", ".jpg", ".jpeg", ".gif",
            ".bmp", ".tiff", ".webp", ".svg"
        },
        "Videos": {
            ".mp4", ".avi", ".mov", ".mkv",
            ".wmv", ".flv", ".webm"
        },
        "Audio": { ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a" },
        "Archives": { ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2" },
        "Executables": { ".exe", ".msi", ".bat", ".sh", ".app" }
    }

    fileList = os.listdir(directory)
    for file in fileList:
        if os.path.isfile(os.path.join(directory, file)):
            splitFile = file.split('.')
            extension = '.' + splitFile[len(splitFile) - 1].lower()
            if sortingAll:
                if not usingGroups:
                    SortFile(directory, target, extension, file)
                else:
                    if usingCustomGroups:
                        foundGroup = False
                        for group in fileGroups:
                            groupName = ', '.join(group)
                            if extension in group:
                                SortFile(directory, target, groupName, file)
                                foundGroup = True
                                break
                        if not foundGroup:
                            SortFile(directory, target, extension, file)

                    else:
                        definition = GetDefinition(extension, fileDefinitions)
                        SortFile(directory, target, definition, file)

            else:
                pass

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
    allFiles = True
    allFilesInput = input("Are you organizing all files, or just a specific set? (ALL/SPECIFIC): ")
    if allFilesInput.lower() == "specific":
        allFiles = False

    print("How will the files be organized?\n1. Alphabetical\n2. File Extension/Type\n3. Date Created\n4. Tags within file names\n5. Word Count (For Documents)")
    userChoice = input('> ')
    match userChoice:
        case '1':
            if allFiles:
                allLettersInput = input("Will you be sorting every letter individually? (Y/N): ")
                if allLettersInput.lower() == 'y':
                    AlphabeticalSort(directoryToOrganize, targetDirectory, allFiles, True)
                else:
                    rangeInput = input("Enter specific letter ranges to sort by (Example: A-D, E-F, G-Z): ")
                    while CheckLetterRange(rangeInput) == False:
                        rangeInput = input("Invalid Range. Please try again: ")
                    rangeInput = rangeInput.replace(" ", "")
                    rangeList = rangeInput.split(',')
                    AlphabeticalSort(directoryToOrganize, targetDirectory, allFiles, False, rangeList)

            else:
                chosenRanges = input("Enter the letter(s) you would like to sort (Example: A, C, G-M): ")
                while True:
                    validLetters = True
                    chosenRanges = chosenRanges.replace(' ', '').split(',')
                    for cRange in chosenRanges:
                        if (len(cRange) == 1 and not cRange.isalpha()) or (len(cRange) != 3 and len(cRange) != 1):
                            validLetters = False
                            break
                    if validLetters:
                        break
                    else:
                        chosenRanges = input("There was an issue with what you entered. Try again (Example: A, C, G-H): ")
                AlphabeticalSort(directoryToOrganize, targetDirectory, allFiles, False, chosenRanges)

        case '2':
            if allFiles:
                filesGrouped = input("Would you like certain file types to be grouped together? (Y/N): ")
                if filesGrouped.upper() == 'Y':
                    customNames = input("Use built-in (Documents, Videos, Images, etc)? (Y/N): ")
                    if customNames.upper() == 'Y':
                        FileTypeSort(directoryToOrganize, targetDirectory, allFiles, True, False)
                    else:
                        fileGroups = []
                        while True:
                            group = input("Add file types to be grouped, separated by commas (.pdf, .txt, .docx). Enter nothing to finish: ")
                            if not group:
                                break
                            group = group.replace(' ', '').split(',')
                            fileGroups.append(group)
                        FileTypeSort(directoryToOrganize, targetDirectory, allFiles, True, True, fileGroups)
                else:
                    FileTypeSort(directoryToOrganize, targetDirectory, allFiles, False, False)

            else:
                fileTypes = input("Provide the type extensions you would like to be organized, spaced by commas (.pdf, .txt, .docx): ")
                grouped = input("Would you like them separated? (Y/N): ")


        case _:
            pass