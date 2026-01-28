import cloudinary.uploader
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import MediaFile

@receiver(post_delete, sender=MediaFile)
def delete_file_from_cloudinary(sender, instance, **kwargs):
    """
    Сигнал спрацьовує ПІСЛЯ видалення запису MediaFile з бази.
    instance — це об'єкт, який щойно був видалений.
    """
    if instance.file:
        # Видаляємо фізичний файл із Cloudinary, використовуючи його public_id
        # У CloudinaryField public_id доступний через .public_id
        public_id = instance.file.public_id
        cloudinary.uploader.destroy(public_id)
        print(f"Файл {public_id} успішно видалений з Cloudinary через сигнал.")