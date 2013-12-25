from django import template
from tradeschool.utils import branch_template

register = template.Library()


def render_field(parser, token):
    render_help = True

    try:
        # split_contents() knows not to split quoted strings.
        args = token.split_contents()
        if len(args) == 3:
            tag_name, branch, field = args
        else:
            tag_name, branch, field, help = args
            if help == 'True':
                render_help = True
            else:
                render_help = False

    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires at least two arguments" % token.contents.split()[0]

    return FieldRenderNode(branch, field, render_help)


class FieldRenderNode(template.Node):
    def __init__(self, branch, field, render_help):
        self.branch = template.Variable(branch)
        self.field = template.Variable(field)
        self.render_help = render_help

    def render(self, context):
        branch = self.branch.resolve(context)
        field = self.field.resolve(context)

        context['field'] = field
        context['render_help'] = self.render_help

        template = branch_template(branch, 'form_field.html')

        html = template.render(context)

        return html


register.tag('render_field', render_field)
