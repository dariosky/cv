import os
from jinja2 import Environment, FileSystemLoader

if __name__ == '__main__':
    # let's get ready for having a static site!
    template_path = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_path),
                            autoescape=True)
    ROUTES = (
        ('cv.html', 'index.html'),
        ('404.html', '404.html'),
    )
    for template_name, output_path in ROUTES:
        template = jinja_env.get_template(template_name)
        with open(output_path, 'w') as o:
            o.write(template.render())
