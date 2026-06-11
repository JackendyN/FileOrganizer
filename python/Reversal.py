import os
from datetime import datetime
import FileMisc


class LogFileError(Exception):
    pass


def start():
    with open("FOLog.txt", 'r') as log_file:
        process_logs = log_file.readlines()
    if not process_logs:
        raise LogFileError("Log file is empty, or is unreachable")

    log_times = {}  # Holds index in process logs for given log time
    for log in process_logs:
        if log[0:2] == "--":
            split_log = log.split()
            log_times[f"{split_log[1]} {split_log[2]} {split_log[3]}"] = process_logs.index(log)

    x = 0
    for time in log_times.keys():
        x += 1
        first_operation = process_logs[log_times[time] + 1]
        print(f"{x}: {time}\nFirst Operation: {first_operation}")

    start_index = 0
    while True:
        process_choice_number = input("Which process should be reverted?\n> ")
        try:
            process_choice_number = int(process_choice_number) - 1
            start_index = list(log_times.values())[process_choice_number] + 1
        except ValueError:
            print("Try entering the number again.")
            continue
        except IndexError:
            print("Try entering the number again.")
            continue
        break

    i = start_index
    failed_attempts = 0
    new_log_list = ["\n-- REVERSAL-" + datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " --\n"]
    while True:
        try:
            if not process_logs[i].rstrip():  # Empty line detected
                break
            if process_logs[i].rstrip() == '.':
                i += 1
                continue
        except IndexError:  # Possible end of file
            break
        process = process_logs[i].split('  ')
        old_location = process[0]
        new_location = process[2].rstrip()
        try:
            os.rename(new_location, old_location)
        except FileNotFoundError:
            failed_attempts += 1
            if failed_attempts == 5:
                FileMisc.log_process(new_log_list)
                raise LogFileError("Process could not be fully reverted.")
        new_log_list.append(new_location + "  =>  " + old_location + "\n")
        i += 1
    FileMisc.log_process(new_log_list)
    print("Done!")
