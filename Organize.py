import os

def AlphabeticalSort(directory, target, sortingAll, allLetters, letterRanges=None):
    fileList = os.listdir(directory)
    if sortingAll:
        for file in fileList:
            if os.path.isfile(os.path.join(directory, file)):
                if allLetters:
                    os.makedirs(os.path.join(target, file[0].upper()), exist_ok=True)
                    newLocation = os.path.join(target, file[0].upper(), file)
                    os.rename(os.path.join(directory, file), newLocation)
                else:
                    targetRange = ""
                    for letterRange in letterRanges:
                        if ord(letterRange[0].upper()) <= ord(file[0].upper()) <= ord(letterRange[2].upper()):
                            targetRange = letterRange
                            break
                    if targetRange == "":
                        continue
                    else:
                        os.makedirs(os.path.join(target, targetRange), exist_ok=True)
                        newLocation = os.path.join(target, targetRange, file)
                        os.rename(os.path.join(directory, file), newLocation)
        print("Done!")


def CheckLetterRange(ranges):
    ranges = ranges.replace(" ", "")
    rangeList = ranges.split(',')
    letterCount = len(rangeList)
    for lRange in rangeList:
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

        case _:
            pass