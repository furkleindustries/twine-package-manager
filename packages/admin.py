from django.contrib import admin

from .models import Package, DeletedPackage, PackageDownload


admin.site.register(Package)
admin.site.register(DeletedPackage)
admin.site.register(PackageDownload)
