from django import template
from django.template.loader import get_template
from tradeschool.forms import DefaultBranchForm

register = template.Library()


def default_branch_form(parser, token):

    try:
        # split_contents() knows not to split quoted strings.
        args = token.split_contents()
        if len(args) == 3:
            tag_name, user, redirect_page = args

    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires at least three arguments" % token.contents.split()[0]

    return DefaultBranchFormNode(user, redirect_page)


class DefaultBranchFormNode(template.Node):
    def __init__(self, user, redirect_page):
        self.user = template.Variable(user)
        self.redirect_page = template.Variable(redirect_page)

    def render(self, context):
        user = self.user.resolve(context)
        redirect_page = self.redirect_page.resolve(context)

        context['form'] = DefaultBranchForm(user, redirect_page)

        template = get_template('tags/default_branch_form.html')

        html = template.render(context)

        return html


register.tag('default_branch_form', default_branch_form)
