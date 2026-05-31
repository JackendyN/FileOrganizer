import os
import time
from datetime import datetime
from enum import Enum

import FileMisc


class SortMethod(Enum):
    ALPHABETICAL = 0
    EXTENSION = 1
    DATE = 2
    TAG = 3


# Isolates file name from any path still possibly attached
def isolate_file(file_path):
    i = file_path.rfind(os.sep)
    if i != -1:
        return file_path[i + 1:]
    else:
        return file_path


def move_file(original_location, target_location, folder_name, file):
    old_location = os.path.join(original_location, file)
    os.makedirs(os.path.join(target_location, folder_name), exist_ok=True)
    new_location = os.path.join(target_location, folder_name, isolate_file(file))
    os.rename(old_location, new_location)
    log = old_location + " => " + str(new_location) + "\n"
    return log


def add_folder_files(directory, original_directory_length):
    files = os.listdir(directory)
    new_files = []
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isdir(file_path):
            new_files += add_folder_files(file_path, original_directory_length)
        elif os.path.isfile(file_path):
            new_files.append(file_path[(original_directory_length + 1):])

    return new_files


def sort_files(directory, target, method, including_folders, all_letters=False, letter_ranges=None, using_groups=False,
               using_custom_groups=False, file_groups=None, name_tag=None, tag_folder=None):
    if including_folders:
        file_list = add_folder_files(directory, len(directory))
    else:
        file_list = os.listdir(directory)
    log_list = ["\n-- " + datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " --\n"]
    for file in file_list:
        if not os.path.isfile(os.path.join(directory, file)):
            continue
        match method:

            # Alphabetical sorting
            case SortMethod.ALPHABETICAL:
                if all_letters:
                    if isolate_file(file)[0].isalpha():
                        log_list.append(move_file(directory, target, isolate_file(file)[0].upper(), file))
                    else:
                        log_list.append(move_file(directory, target, "Misc", file))
                else:
                    temp_file = isolate_file(file)
                    target_range = ""
                    for letter_range in letter_ranges:
                        if not file[0].isalpha():
                            break
                        if ((len(letter_range) == 1 and temp_file[0].upper() == letter_range)
                                or (len(letter_range) != 1 and (
                                        ord(letter_range[0].upper()) <= ord(temp_file[0].upper()) <= ord(letter_range[2].upper())))):
                            target_range = letter_range
                            break
                    if target_range == "":
                        log_list.append(move_file(directory, target, "Misc", file))
                    else:
                        log_list.append(move_file(directory, target, target_range, file))

            # File extension sorting
            case SortMethod.EXTENSION:
                split_file = file.split('.')
                extension = '.' + split_file[len(split_file) - 1].lower()
                if not using_groups:
                    log_list.append(move_file(directory, target, extension, file))
                else:
                    if using_custom_groups:
                        found_group = False
                        for group in file_groups:
                            group_name = ','.join(group)
                            if extension in group:
                                log_list.append(move_file(directory, target, group_name, file))
                                found_group = True
                                break
                        if not found_group:
                            log_list.append(move_file(directory, target, extension, file))

                    else:
                        definition = FileMisc.get_file_definition(extension)
                        log_list.append(move_file(directory, target, definition, file))

            # File date sorting
            case SortMethod.DATE:
                months = ("January", "February", "March", "April", "May", "June", "July", "August", "September",
                          "October", "November", "December")
                file_time = time.localtime(os.path.getctime(os.path.join(directory, file)))
                if using_groups:
                    log_list.append(
                        move_file(directory, target, f"{months[file_time.tm_mon - 1]} {file_time.tm_year}", file))
                else:
                    log_list.append(move_file(directory, target, f"{file_time.tm_year}", file))

            # Sorting files with a certain tag in their name
            case SortMethod.TAG:
                isolated_file = isolate_file(file)
                extension_start = isolated_file.rfind('.')
                isolated_file = isolated_file[0:extension_start]
                if name_tag.lower() in isolated_file.lower():
                    if not tag_folder:
                        log_list.append(move_file(directory, target, name_tag, file))
                    else:
                        log_list.append(move_file(directory, target, tag_folder, file))

    FileMisc.log_process(log_list)
    print("Done!")


def check_letter_range(ranges):
    ranges = ranges.replace(" ", "")
    range_list = ranges.split(',')
    letter_count = len(range_list)
    for l_range in range_list:
        if len(l_range) != 3:
            return False
        if not (l_range[2].isalpha and l_range[0].isalpha):
            return False
        letter_count += (ord(l_range[2].upper()) - ord(l_range[0].upper()))
    return letter_count == 26


def start():
    directory_to_organize = input("Directory to organize: ")
    while not os.path.exists(directory_to_organize):
        directory_to_organize = input("The directory to organize you entered does not exist. Please enter it again: ")
    target_directory = directory_to_organize
    same_place_input = input("Put folders in same directory? (Y/N): ")
    if same_place_input.upper() != 'Y':
        target_directory = input("Target directory: ")
        while not os.path.exists(target_directory):
            target_directory = input(
                "The target directory to put the organized files in does not exist. Please try again: ")
    folders_input = input("Include files already inside folders? (Y/N): ")
    include_folders = False
    if folders_input.upper() == 'Y':
        include_folders = True

    print(
        "How will the files be organized?\n1. Alphabetical\n2. File Extension/Type\n3. Date Created\n4. Tags within "
        "file names\n")
    user_choice = input('> ')
    match user_choice:

        case '1':
            all_letters_input = input("Will you be sorting every letter individually? (Y/N): ")
            if all_letters_input.lower() == 'y':
                sort_files(directory_to_organize, target_directory, SortMethod.ALPHABETICAL, include_folders,
                           all_letters=True)
            else:
                range_input = input("Enter specific letter ranges to sort by (Example: A-D, E-F, G-Z): ")
                while not check_letter_range(range_input):
                    range_input = input("Invalid Range. Please try again: ")
                range_input = range_input.replace(" ", "")
                range_list = range_input.split(',')
                sort_files(directory_to_organize, target_directory, SortMethod.ALPHABETICAL, include_folders,
                           letter_ranges=range_list)

        case '2':
            files_grouped = input("Would you like certain file types to be grouped together? (Y/N): ")
            if files_grouped.upper() == 'Y':
                custom_names = input("Use built-in (Documents, Videos, Images, etc)? (Y/N): ")
                if custom_names.upper() == 'Y':
                    sort_files(directory_to_organize, target_directory, SortMethod.EXTENSION, include_folders,
                               using_groups=True, using_custom_groups=False)
                else:
                    file_groups = []
                    while True:
                        group = input(
                            "Add file types to be grouped, separated by commas (.pdf, .txt, .docx). Enter nothing to "
                            "finish: ")
                        if not group:
                            break
                        group = group.replace(' ', '').split(',')
                        file_groups.append(group)
                    sort_files(directory_to_organize, target_directory, SortMethod.EXTENSION, include_folders,
                               using_groups=True, using_custom_groups=True, file_groups=file_groups)
            else:
                sort_files(directory_to_organize, target_directory, SortMethod.EXTENSION, include_folders)

        case '3':
            date_sort_choice = input("Would you like to sort by month or year? (MONTH/YEAR): ").lower()
            while date_sort_choice != ("month" or "year"):
                date_sort_choice = input("Try again (MONTH/YEAR): ").lower()
            if date_sort_choice == "month":
                sort_files(directory_to_organize, target_directory, SortMethod.DATE, include_folders, using_groups=True)
            else:
                sort_files(directory_to_organize, target_directory, SortMethod.DATE, include_folders, using_groups=False)

        case '4':
            tag = input("Include files with what in their file name? (Example: *HIST 1101* Essay 1): ")
            folder_name = input("What should the folder be called? (Leave blank to use tag given): ")
            sort_files(directory_to_organize, target_directory, SortMethod.TAG, include_folders, name_tag=tag,
                       tag_folder=folder_name)

        case _:
            print("Invalid choice.")
