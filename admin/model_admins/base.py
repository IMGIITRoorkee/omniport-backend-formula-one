import swapper
from django.contrib import admin
from django.contrib.admin.widgets import (
    AutocompleteSelect,
    AutocompleteSelectMultiple,
)

from base_auth.models import User

Person = swapper.load_model('kernel', 'Person')
Student = swapper.load_model('kernel', 'Student')
FacultyMember = swapper.load_model('kernel', 'FacultyMember')

class ModelAdmin(admin.ModelAdmin):
    """
    This class extends Django's ModelAdmin class to replace all ForeignKey
    select widget with an autocomplete widget
    """

    """
    A list of models that have way too many entries in the database to be
    loaded via select widgets and would benefit from autocomplete fields
    """
    large_models = [
        Person,
        User,
        Student,
        FacultyMember,
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Specify AutocompleteSelect widget if related model has many
        entries and defer to the base implementation of the function
        :param db_field: the ForeignKey whose field is being determined
        :param request: the request object establishing the context
        :param kwargs: keyword arguments to customise the determination
        :return: the formfield for this ForeignKey
        """

        db = kwargs.get('using')

        if db_field.related_model in self.large_models:
            kwargs['widget'] = AutocompleteSelect(
                db_field.remote_field,
                self.admin_site,
                using=db,
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Specify AutocompleteSelectMultiple widget if related model has many
        entries and defer to the base implementation of the function
        :param db_field: the ManyToManyField whose field is being determined
        :param request: the request object establishing the context
        :param kwargs: keyword arguments to customise the determination
        :return: the formfield for this ManyToManyField
        """

        db = kwargs.get('using')

        if db_field.related_model in self.large_models:
            kwargs['widget'] = AutocompleteSelectMultiple(
                db_field.remote_field,
                self.admin_site,
                using=db,
            )

        return super().formfield_for_manytomany(db_field, request, **kwargs)
