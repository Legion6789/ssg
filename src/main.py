import shutil
import os


def copy_static():
    shutil.rmtree("/home/legion/Development/ssg/public", True)
    shutil.copytree(
        "/home/legion/Development/ssg/static", "/home/legion/Development/ssg/public"
    )


def main():
    copy_static()


main()
