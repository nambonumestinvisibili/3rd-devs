import html2text

input_file = "1-article.html"
output_file = "3-article.md"

with open(input_file, "r", encoding="utf-8") as f:
  html_content = f.read()

h = html2text.HTML2Text()
h.body_width = 0  # Prevent line wrapping
h.ignore_links = False  # Keep links
h.ignore_images = False  # Keep images

markdown = h.handle(html_content)

with open(output_file, "w", encoding="utf-8") as f:
  f.write(markdown)