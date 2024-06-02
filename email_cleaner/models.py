from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=999)
    default_activity = models.CharField(max_length=999, choices=[("NEW","NEW"), ("DELETE","DELETE"), ("MARK AS READ","MARK AS READ")])
    
    def get_email_count(self):
        return self.email_set.count()

    def __str__(self):
        return self.name

class Email(models.Model):
    external_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    sender = models.ForeignKey(Contact, on_delete=models.CASCADE)
    subject = models.CharField(max_length=9999, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    snippet = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=999, choices=[("NEW", "NEW"), ("DELETED", "DELETED"), ("MARKED AS READ", "MARKED AS READ")], default="NEW")
    auto_generated_category = models.CharField(max_length=999, null=True, blank=True)
    auto_generated_summary = models.TextField(null=True, blank=True)
    auto_generated_blog_ideas = models.TextField(null=True, blank=True)


class SettingValue(models.Model):
    setting_name = models.CharField(max_length=999)
    setting_value = models.CharField(max_length=999, null=True, blank=True)

    def __str__(self):
        return self.setting_value or "False"
