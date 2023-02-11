from datetime import datetime

from peewee import DateField, Model

from config import ConfigClass


class BaseModel(Model):
    create_at = DateField()
    updated_at = DateField()
    is_deleted = False

    def delete(self):
        self.is_deleted = True
        return self.save()

    def save(self, *args, **kwargs):
        if self.create_at is None:
            self.create_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.updated_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        database = ConfigClass.DATABASE
        abstract = True


class BaseModelNoSoftDelete(BaseModel):
    is_deleted = None

    def delete(self):
        return super().delete()

    class Meta:
        abstract = True
