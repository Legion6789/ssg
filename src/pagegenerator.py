from nodehelper import NodeHelper
import os


def extract_title(markdown):
    lines = markdown.split("\n")
    if len(lines) == 0 or not lines[0].startswith("# "):
        raise Exception('missing title (no "# " at start of file)')
    return lines[0][2:]


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {
          dest_path} using {template_path}")
    markdown = get_file_data(from_path)
    template = get_file_data(template_path)
    html = NodeHelper.markdown_to_html_node(markdown).to_html()
    html = html.replace("<li> ", "<li>")
    html = html.replace("<blockquote> ", "<blockquote>")
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    write_file_data(dest_path, template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(
        f"Generating page from {dir_path_content} to {dest_dir_path} using {
            template_path
        }"
    )
    md_files = get_all_md_files(dir_path_content)
    for md_file in md_files:
        markdown = get_file_data(md_file)
        template = get_file_data(template_path)
        html = NodeHelper.markdown_to_html_node(markdown).to_html()
        html = html.replace("<li> ", "<li>")
        html = html.replace("<blockquote> ", "<blockquote>")
        title = extract_title(markdown)
        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", html)
        html_file = f"{md_file[:-3]}.html"
        html_file = html_file.replace("content", "public")
        write_file_data(html_file, template)


def get_all_md_files(dir_path_content):
    md_files = []

    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.abspath(os.path.join(root, file))
                md_files.append(full_path)
    return md_files


def get_file_data(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def write_file_data(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
