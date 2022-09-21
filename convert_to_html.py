import os
from bs4 import BeautifulSoup
import mdtex2html

with open("template.html", "r") as file:
    template = file.read()

for root, subdirs, files in os.walk("src/"):
    # print(root, subdirs, files)
    new_root = root.replace("src/", "")
    try:
        if root != "src/":
            os.mkdir(new_root)
    except FileExistsError:
        pass
    for filename in files:
        if filename[-3:] == ".md":
            with open(os.path.join(root, filename), "r") as file:
                markdown_content = file.read()
            html_content = mdtex2html.convert(markdown_content)
            soup = BeautifulSoup(html_content, "html.parser")
            for a in soup.find_all("a"):
                href = a["href"]
                if (href[:4] != "http") and href[-3:] == ".md":
                    new_href = "/" + href.replace(".md", ".html")
                    html_content = html_content.replace(href, new_href)

            for img in soup.find_all("img"):

                img_text = str(img)[:-2] + " />"
                new_img_text = (
                    "<div class=\"img-container\">" + img_text + "</div>"
                )
                html_content = html_content.replace(img_text, new_img_text)

            html_content = template.replace("HTML_CONTENT", html_content)
        new_filename = filename.replace(".md", ".html")

        with open(os.path.join(new_root, new_filename), "w") as file:
            file.write(html_content)
