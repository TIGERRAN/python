#coding:utf-8

from django import template

register = template.Library()

class upperNode(template.Node):
    def __init__(self,nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        a = content.split(',')
        res1 = float(a[0])*float(a[1])
        res2 = '{:.2f}'.format(res1)
        return res2


@register.tag
def multiplication(parser,token):
    nodelist = parser.parse("endmultiplication") #指定结束符
    parser.delete_first_token()

    return upperNode(nodelist)