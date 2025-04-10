import shutil
from pagegenerator import generate_page, generate_pages_recursive
import sys


def copy_static(filepath):
    shutil.rmtree(f"{filepath}docs", True)
    shutil.copytree(f"{filepath}static", f"{filepath}docs")


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    filepath = "/home/legion/Development/ssg/"
    copy_static(filepath)
    # generate_page(
    #    f"{filepath}content/index.md",
    #    f"{filepath}template.html",
    #    f"{filepath}docs/index.html",
    #    basepath
    # )
    generate_pages_recursive(
        f"{filepath}content/",
        f"{filepath}template.html",
        f"{filepath}docs/",
        basepath,
    )


main()
