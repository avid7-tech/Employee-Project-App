from django.db import models

class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True)

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return self.update(is_deleted=False)

    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.filter(is_deleted=True)
    
    

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()

    def get_all_active_employees(self):
        return self.get_queryset().filter(active=True)

    def get_all_objects(self):
        return self.get_queryset().alive()

    def deleted_objects(self):
        return self.get_queryset().dead()
