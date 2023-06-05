from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Professeur, Etudiant
from account.models import Account,DemandeAcces


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'user_type')
    search_fields = ('email', 'username', 'user_type')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'date_inscription')

class DemandeAccesAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_demande', 'accepte')
    list_filter = ('accepte',)
    actions = ['accept_requests', 'delete_requests']

    def accept_requests(self, request, queryset):
        queryset.update(accepte=True)  
        for demande_acces in queryset:
            demande_acces.accepte = True
            demande_acces.save()
            professeur = Professeur.objects.create(email=demande_acces.user.email, user=demande_acces.user)
            professeur.save()
        queryset.delete()

    accept_requests.short_description = "Accept selected requests"

    def delete_requests(self, request, queryset):
        queryset.delete()

    delete_requests.short_description = "Delete selected requests"


admin.site.register(Account,AccountAdmin)
admin.site.register(Professeur)
admin.site.register(Etudiant,EtudiantAdmin)
admin.site.register(DemandeAcces, DemandeAccesAdmin)
