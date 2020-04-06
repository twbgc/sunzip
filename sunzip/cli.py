import argparse
import sunzip

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_file", help="the zip archive to unzip safely")
    parser.add_argument(
        "-mc",
        "--max-compression-ratio",
        help="the max compression ratio to trust.",
        type=int,
    )
    parser.add_argument(
        "-ms",
        "--max-cpu-seconds",
        help="the max amount of seconds to process on the cpu.",
        type=int,
    )
    parser.add_argument(
        "-mm",
        "--max-memory-bytes",
        help="the max amount bytes of RAM to use for decompression",
        type=int,
    )
    parser.add_argument(
        "-md",
        "--max-disk-space-bytes",
        help="the max amount bytes of disk space to use for decompression",
        type=int,
    )
    args = parser.parse_args()

    zip_archive = sunzip.sunzip(args.zip_file)

    if args.max_compression_ratio:
        zip_archive.threshold = args.max_compression_ratio
    if args.max_cpu_seconds:
        zip_archive.cpu =  args.max_cpu_seconds
    if args.max_memory_bytes:
        zip_archive.memory = args.max_memory_bytes
    if args.max_disk_space_bytes:
        zip_archive.filesize  = args.max_disk_space_bytes

    zip_archive.extract()
