from django.db import models
#-------------------------------------------------------------------------------------------------
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')
#-------------------------------------------------------------------------------------------------

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)