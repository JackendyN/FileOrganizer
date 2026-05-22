# Creates a folder on the desktop with randomly named files for testing purposes, replaces it if it already exists, then optionally sorts it
# not responsible for anything that happens if you try actually opening these files so please don't
import os
import shutil
import random
import string
import Organize

extensions = (".doc", ".docx", ".pdf", ".txt", ".rtf", ".odt", ".pages", ".md", ".py", ".java", ".cs", ".cpp", ".c",
              ".xls", ".xlsx", ".csv", ".ods", ".ppt", ".pptx", ".key", ".png", ".jpg", ".jpeg", ".mp4", ".avi", ".mov",
              ".mp3", ".wav", ".aac", ".zip", ".rar", ".exe", ".msi", ".bat")
testDirectory = os.path.join(os.path.expanduser("~"), "Desktop", "jnfoctffiles")
shutil.rmtree(testDirectory, ignore_errors=True)
os.makedirs(testDirectory, exist_ok=False)
for i in range(300):
    fileName = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + random.choice(extensions)
    open(os.path.join(testDirectory, fileName), 'w')
# Organize.SortFiles(testDirectory, testDirectory, Organize.SortMethod.EXTENSION, True, usingGroups=True)
print("Done!")