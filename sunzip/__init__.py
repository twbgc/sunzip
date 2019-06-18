# Author: JunWeiSong, KunYuChen
# Provide secure unzip against zip bomb. Once it detects,it will ignore
# the malicious file and raise an error.
import os.path
import resource
import sys
import zipfile

# 1 second
MAX_CPU_USAGE = 1
# 134217728 bytes (128MB)
MAX_MEMORY_USAGE = 134217728
# 134217728 bytes (128MB)
MAX_FILESIZE_USAGE = 134217728
# Compression ratio
MAX_THRESHOLD = 100


class sunzip():

    def __init__(self, path, method=None):
        """
        path: The path parameter is the absolute position of the file where the
        zip file is located.

        method: The method parameter is the algorithm that determines the
        compression, default is Deflate.
        """
        self.path = path
        self.method = method
        self.zip_file = zipfile.ZipFile(path, "r")
        self.max_threshold = MAX_THRESHOLD
        self.max_cpu_usage = MAX_CPU_USAGE
        self.max_mem_usage = MAX_MEMORY_USAGE
        self.max_filesize_usage = MAX_FILESIZE_USAGE

    def check_is_zipfile(self):
        # Check if it's a real zip file.
        # Return True when it is a real zip file

        if (zipfile.is_zipfile(self.path)):
            return True
        else:
            raise ZipFilePitfall("File does not match to zip format.")

    def check_is_nested(self):
        # Check if it's a nested zip file. (i.e. 42.zip)
        # Return True when there is no nested zip file.
        for f in self.zip_file.namelist():
            if(os.path.splitext(f)[1] == ".zip"):
                raise ZipFilePitfall("Found a nested compressed file.")
            else:
                return True

    def get_zip_file_size(self):
        # Return undecompressd zip file size
        return os.stat(self.path).st_size

    def get_uncompressed_size(self):
        # Return the file size before compression.
        return sum(zp.file_size for zp in self.zip_file.infolist())

    def get_compressed_size(self):
        # Return the file size after compression.
        return sum(zp.compress_size for zp in self.zip_file.infolist())

    def get_compression_ratio(self):
        # Return compression ratio of the zip file.
        try:
            return self.get_uncompressed_size() / self.get_compressed_size()
        except ZeroDivisionError:
            return 0

    @property
    def threshold(self):
        return self.max_threshold

    @property
    def cpu(self):
        return self.max_cpu_usage

    @property
    def memory(self):
        return self.max_mem_usage

    @property
    def filesize(self):
        return self.max_filesize_usage

    @threshold.setter
    def threshold(self, threshold_limit):
        self.max_threshold = threshold_limit

    @cpu.setter
    def cpu(self, cpu_limit):
        self.max_cpu_usage = cpu_limit

    @memory.setter
    def memory(self, memory_limit):
        self.max_mem_usage = memory_limit

    @filesize.setter
    def filesize(self, filesize_limit):
        self.max_filesize_usage = filesize_limit

    def _limit_source(self):
        # Limit available resources.

        # CPU
        resource.setrlimit(resource.RLIMIT_CPU,
                           (self.max_cpu_usage, self.max_cpu_usage))
        # MEMORY
        resource.setrlimit(resource.RLIMIT_AS,
                           (self.max_mem_usage, self.max_mem_usage))
        # FILESIZE
        resource.setrlimit(resource.RLIMIT_FSIZE,
                           (self.max_filesize_usage, self.max_filesize_usage))

    def extract(self):
        # Unzip the zip file in a secure way. It would unzip the zip file only
        # if the status is True after all checks have passed.

        status = False
        threshold = self.threshold

        # Defense Layer 1 - checks perform on the server side.

        # Check if the file format is expected for context.

        try:
            if(self.check_is_zipfile()):
                status = True
            else:
                raise ZipFilePitfall("File type is not zip format.")
        except Exception as e:
            print(e)
            sys.exit(0)

        # Check if it's a nested zip file.
        try:
            if(self.check_is_nested()):
                status = True
            else:
                raise ZipFilePitfall("Zip file contains nested zip file.")
        except Exception as e:
            print(e)
            sys.exit(0)

        # Check if the compression ratio is greater than threshold.
        try:
            if(self.get_compression_ratio() <= self.max_threshold):
                status = True
            else:
                raise ZipFilePitfall(
                    "Compression ratio is greater than threshold.")
        except Exception as e:
            print(e)
            sys.exit(0)

        # Check if the upload file size exceeds the maximum limit.
        try:
            if(self.get_zip_file_size() <= self.max_filesize_usage):
                status = True
            else:
                raise ZipFilePitfall(
                    "File size exceeds the maximum limit.")
        except Exception as e:
            print(e)
            sys.exit(0)

        # Defense Layer 2 - Limit the number of resources available to a
        # process and its child process.

        self._limit_source()

        # Defense Layer 3 - Filetype-specific mitigations.
        if (status is True):
            print("All rules have checked completely. Start to unzipping.")
            self.zip_file.extractall()


class ZipFilePitfall(Exception):
    # Raise error usage.
    pass


if __name__ == "__main__":
    """
    CLI Usage: python main.py archive.zip.
    """

    if(len(sys.argv) == 2):

        unzipfile = sys.argv[1]

        zi = sunzip(unzipfile)

        zi.extract()
    else:
        print("CLI Usage: python main.py archive.zip.")
