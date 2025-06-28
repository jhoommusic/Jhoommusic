import os


def dirr():
    if "downloads" not in os.listdir():
        os.makedirs("downloads")
    if "cache" not in os.listdir():
        os.makedirs("cache")
    if "raw_files" not in os.listdir():
        os.makedirs("raw_files")