# stuff I decided to move to a separate file to keep others cleaner

def GetDefinition(extension):
    for definition, extensions in fileDefinitions.items():
        if extension in extensions:
            return definition
    return "Other"

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