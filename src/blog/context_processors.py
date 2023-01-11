
def categories(request):
    from blog.models import Category
    return {'categories': Category.objects.all()}