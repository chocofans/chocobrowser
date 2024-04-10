class HTMLParser:
    def parse(self, html):
        # A very basic HTML parser that simply looks for opening and closing tags
        stack = []
        root = None
        current_parent = None

        for token in html.split('<'):
            if token.startswith('/'):
                # Closing tag
                tag_name = token.split('>')[0][1:]
                if stack and stack[-1].tag == tag_name:
                    stack.pop()
                    if stack:
                        current_parent = stack[-1]
                else:
                    raise ValueError("Invalid HTML")

            elif token:
                # Opening tag
                parts = token.split('>')
                tag_name = parts[0]
                attributes = {}
                if len(parts) > 1:
                    attributes = self.extract_attributes(parts[0])
                element = HTMLElement(tag_name, attributes)
                if not root:
                    root = element
                if current_parent:
                    current_parent.children.append(element)
                stack.append(element)
                current_parent = element

        return root

    def extract_attributes(self, token):
        attributes = {}
        parts = token.split()
        if len(parts) > 1:
            for part in parts[1:]:
                key, value = part.split('=')
                attributes[key] = value.strip('"\'')
        return attributes


class HTMLElement:
    def __init__(self, tag, attributes=None, children=None):
        self.tag = tag
        self.attributes = attributes or {}
        self.children = children or []


class HTMLRenderer:
    def render(self, element, indent=0):
        # Basic renderer to display the HTML structure
        if element:
            print(' ' * indent + f"<{element.tag}>")
            for child in element.children:
                self.render(child, indent + 4)
            print(' ' * indent + f"</{element.tag}>")


class HTMLDocument:
    def __init__(self):
        self.root = None

    def load(self, html):
        parser = HTMLParser()
        self.root = parser.parse(html)

    def render(self):
        renderer = HTMLRenderer()
        renderer.render(self.root)


# Test the implementation
html_content = """
<html>
<head>
<title>Sample HTML Page</title>
</head>
<body>
<h1>Hello, World!</h1>
<p>This is a sample HTML page.</p>
</body>
</html>
"""

doc = HTMLDocument()
doc.load(html_content)
doc.render()
