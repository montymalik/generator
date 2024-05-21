import os
from pathlib import Path

from block_markdown import markdown_to_html_node


def generate_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:]
    else:
        raise Exception("h1 header required")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page fom {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        content = file.read()

    with open(template_path, 'r') as file:
        template = file.read()

    html_node = markdown_to_html_node(content)
    html = html_node.to_html()
    title = generate_title(content)

    with open(dest_path, 'w') as file:
        file.write(template.replace("{{ Title }}",
                                    title).replace("{{ Content }}", html))


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(from_path):
            if Path(from_path).suffix == ".md":
                dest_path = os.path.join(dest_dir_path, f"{Path(from_path).stem}.html")
                generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, os.path.join(dest_dir_path, filename))