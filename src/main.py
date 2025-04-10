import shutil
from pagegenerator import generate_page, generate_pages_recursive


def copy_static():
    shutil.rmtree("/home/legion/Development/ssg/public", True)
    shutil.copytree(
        "/home/legion/Development/ssg/static", "/home/legion/Development/ssg/public"
    )


def main():
    copy_static()
    path_prefix = "/home/legion/Development/ssg"
    # generate_page(
    #    f"{path_prefix}/content/index.md",
    #    f"{path_prefix}/template.html",
    #    f"{path_prefix}/public/index.html",
    # )
    generate_pages_recursive(
        f"{path_prefix}/content/",
        f"{path_prefix}/template.html",
        f"{path_prefix}/public/",
    )


main()
