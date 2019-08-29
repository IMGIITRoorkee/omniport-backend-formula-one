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
        :param args: arguments
        :param kwargs: keyword arguments, including whether to run validations
        """
        
        self._run_validations = kwargs.pop('run_validations', False)
        
        return super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Override save method of FacultyMember class to automatically
        run validations on a model if opted in.
        :param args: arguments
        :param kwargs: keyword arguments, including whether to run validations
        :return: the output of the function from base class
        """

        if self._run_validations or kwargs.pop('run_validations', False):
            self.full_clean()

        return super().save(*args, **kwargs)
