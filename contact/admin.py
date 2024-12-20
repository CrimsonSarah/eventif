from django.contrib import admin
from django.utils.timezone import now
from contact.models import Contact



class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message',
                    'sent_at', 'response', 'response_at', 'respondeu_contato')
    list_editable = ['response']
    date_hierarchy = 'sent_at'
    search_fields = ('name', 'email', 'phone', 'message', 'response', 'response_at', 'sent_at')
    
    def respondeu_contato(self, obj):
        return obj.response != None

    respondeu_contato.short_description = 'Contato respondido'
    respondeu_contato.boolean = True

    def campo_para_db(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "response":
            field.widget = forms.Textarea(attrs={'name':'body', 'rows':'3', 'cols':'15'})
        return field

admin.site.register(Contact, ContactModelAdmin)
