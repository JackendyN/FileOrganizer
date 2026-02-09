import os

def SortFile(originalLocation, targetLocation, folderName, file):
    os.makedirs(os.path.join(targetLocation, folderName), exist_ok=True)
    newLocation = os.path.join(targetLocation, folderName, file)
    os.rename(os.path.join(originalLocation, file), newLocation)

def AlphabeticalSort(directory, target, sortingAll, allLetters, letterRanges=None):
    fileList = os.listdir(directory)
    for file in fileList:
        if os.path.isfile(os.path.join(directory, file)):
            if allLetters:
                SortFile(directory, target, file[0].upper, file)
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

    print("How will the files be organized?\n1. Alphabetical\n2. File Type\n3. Date Created\n4. Tags within file names\n5. Word Count (For Documents)")
    userChoice = input('> ')
    match userChoice:
        case '1':
            if allFiles:
                allLetters = False
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
                    chosenRanges = chosenRanges.replace(' ', '')
                    chosenRanges = chosenRanges.split(',')
                    for cRange in chosenRanges:
                        if (len(cRange) == 1 and not cRange.isalpha()) or (len(cRange) != 3 and len(cRange) != 1):
                            validLetters = False
                            break
                    if validLetters:
                        break
                    else:
                        chosenRanges = input("There was an issue with what you entered. Try again (Example: A, C, G-H): ")
                AlphabeticalSort(directoryToOrganize, targetDirectory, allFiles, False, chosenRanges)


        case _:
            pass