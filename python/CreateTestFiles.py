# Creates a folder on the desktop with randomly named files for testing purposes
import os
import random
import shutil
import string

extensions = (".doc", ".docx", ".pdf", ".txt", ".rtf", ".odt", ".pages", ".md", ".py", ".java", ".cs", ".cpp", ".c",
              ".xls", ".xlsx", ".csv", ".ods", ".ppt", ".pptx", ".key", ".png", ".jpg", ".jpeg", ".mp4", ".avi", ".mov",
              ".mp3", ".wav", ".aac", ".zip", ".rar", ".exe", ".msi", ".bat")
test_directory = os.path.join(os.path.expanduser("~"), "Desktop", "jnfoctffiles")
shutil.rmtree(test_directory, ignore_errors=True)
os.makedirs(test_directory, exist_ok=False)
for i in range(300):
    file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + random.choice(extensions)
    open(os.path.join(test_directory, file_name), 'w')
print("Done!")
