from home.models import Category,Logo
def categories(request):
    logo=Logo.objects.first()
    categoris = Category.objects.active()
    return{"categoris":categoris,'logo':logo}