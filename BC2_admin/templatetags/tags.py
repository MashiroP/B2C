from django import template

from BC2_admin.models import category, category_Subcategory

register = template.Library()
from django.utils.html import format_html

@register.simple_tag
def a ():
	context = { }
	context ['category'] = category.objects.all( )
	s=''
	for i in context ['category']:
		context ['category_Subcategory'] = category_Subcategory.objects.filter(uid=i.id)
		
	for i in context ['category']:
		s+="""
		 <li class="parent">
                <a href="">{u}</a>
		""".format(u=i.category_father)
		for c in i.category_subcategory_set.all():

			s +='''<ul class="sub">
				   <li><a href="">{sa}</a></li>
				   </ul>
					</li>
			'''.format(sa=c.Subgrade_name)

			
		return format_html(s)