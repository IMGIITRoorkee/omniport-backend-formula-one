from django.db import models


class Model(models.Model):
    """
    This abstract root model should be inherited by all model classes
    Provides additional features like soft delete and datetime information
    Do not inherit from django.db.models.Model!
    """

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for Model
        """

        abstract = True

    def __init__(self, *args, **kwargs):
        """
        Delegate to superclass after checking for a keyword argument
        to run validations on model save method.
        :param kwargs: accepts an argument to toggle model validations
        """
        self._run_validations = kwargs.get('run_validations', False)
        kwargs.pop('run_validations', False)
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Override save method of FacultyMember class to automatically
        run validators of a model.
        :param kwargs: accepts an argument to toggle model validations
        :return:
        """

        if self._run_validations or kwargs.get('run_validations', False):
            self.full_clean()
        return super().save(*args, **kwargs)
