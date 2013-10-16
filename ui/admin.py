from django.contrib import admin

from ui.models import ProcessingSession, Item, Project, \
        UserProfile


admin.site.register(Project)
admin.site.register(Item)
admin.site.register(ProcessingSession)
admin.site.register(UserProfile)

