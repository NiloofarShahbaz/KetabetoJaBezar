# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Book,User_Book
#
# @receiver(post_save, sender=Book)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         User_Book.objects.create(book=instance)
#
# @receiver(post_save, sender=Book)
# def save_user_profile(sender, instance, **kwargs):
#     instance.User_Book.save()
