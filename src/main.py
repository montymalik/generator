from textnode import TextNode
import shutil
import os
from page_generation import generate_pages_recursive
from copy_static import copy_files_recursive


src_dir = './static'
dst_dir = './public'


def main():
    print("Deleting public directory...")
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    print("Copying")
    copy_files_recursive(src_dir, dst_dir)

    generate_pages_recursive("./content", "./template.html", dst_dir)


if __name__ == "__main__":
    main()
