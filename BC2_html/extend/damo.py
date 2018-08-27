from BC2_admin.models import category, category_Subcategory


def a ():
    context = { }
    context ['category'] = category.objects.all( )
    for i in context ['category']:
        context ['category_Subcategory'] = category_Subcategory.objects.filter(uid=i.id)
    return context