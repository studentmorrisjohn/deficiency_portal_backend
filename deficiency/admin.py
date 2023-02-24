from django.contrib import admin
from deficiency.models import Deficiency, DocumentDeficiency, FinanceDeficiency
# Register your models here.
admin.site.register(Deficiency)
admin.site.register(DocumentDeficiency)
admin.site.register(FinanceDeficiency)
