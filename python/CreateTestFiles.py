# Creates a folder on the desktop with randomly named files for testing purposes
import os
import random
import string

extensions = (".doc", ".docx", ".pdf", ".txt", ".rtf", ".odt", ".pages", ".md", ".py", ".java", ".cs", ".cpp", ".c")
testDirectory = os.path.join(os.path.expanduser("~"), "Desktop", "FOTest")
try:
    os.makedirs(testDirectory, exist_ok=False)
    for i in range(300):
        fileName = ''.join(random.choices(string.ascii_lowercase, k=8)) + random.choice(extensions)
        open(os.path.join(testDirectory, fileName), 'w')
    print("Done!")

except FileExistsError:
    print("Test folder already exists")