from jinja2 import Environment, FileSystemLoader

templates = Environment(loader=FileSystemLoader("apps/email_events/templates"))