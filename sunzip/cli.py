import argparse
import sunzip

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_file", help="the zip archive to unzip safely")
    args = parser.parse_args()
    
    zip_archive = sunzip.sunzip(args.zip_file)
    zip_archive.extract()
