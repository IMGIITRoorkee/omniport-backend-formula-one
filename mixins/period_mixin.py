import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models import Q, Model
from django.core.exceptions import ValidationError

from formula_one.enums.active_status import ActiveStatus


class PeriodMixin(Model):
    """
    This mixin adds information about the start and end of any entity's
    active period
    """

    start_date = models.DateField()
    # A blank end date denotes that the end date is not known and in the future
    end_date = models.DateField(
        blank=True,
        null=True,
    )

    class Meta:
        """
        Meta class for PeriodMixin
        """

        abstract = True

    def clean(self):
        """
        Hook for checking if the end date of a period is after or same as
        start date
        :raise: ValidationError, if end date is before start date
        """

        if (self.end_date is not None) and (self.end_date < self.start_date):
            raise ValidationError({
                'end_date': 'End date cannot be before start date.'
            })

    def save(self, *args, **kwargs):
        """
        Override save method to check the custom validations written in clean
        method
        """

        # Intrinsically calls the `clean` method
        self.full_clean()
        return super().save(*args, **kwargs)

    @classmethod
    def objects_filter(cls, active_status):
        """
        Return a query set of objects that match the specified active status
        :param active_status: the active status of objects to keep in the set
        :return: a query set of objects with the specified active status
        """

        if hasattr(cls, 'objects'):
            today = datetime.date.today()

            if ActiveStatus.HAS_BEEN_ACTIVE in active_status:
                q_has_been_active = Q(end_date__lt=today)
            else:
                q_has_been_active = Q()

            if ActiveStatus.IS_ACTIVE in active_status:
                q_start = Q(start_date__lte=today)
                q_end_missing = Q(end_date=None)
                q_end_not_passed = Q(end_date__gte=today)
                q_end = Q(q_end_missing | q_end_not_passed)
                q_is_active = Q(q_start & q_end)
            else:
                q_is_active = Q()

            if ActiveStatus.WILL_BE_ACTIVE in active_status:
                q_will_be_active = Q(start_date__gt=today)
            else:
                q_will_be_active = Q()

            q = q_has_been_active | q_is_active | q_will_be_active
            return cls.objects.filter(q)
        else:
            raise AttributeError('Class does not have attribute \'objects\'')

    @property
    def is_active(self):
        """
        Return whether the entity is currently active
        :return: True if start date has passed and end date has not
        """

        today = datetime.date.today()
        if self.end_date is not None:
            return self.start_date <= today <= self.end_date
        else:
            return self.start_date <= today

    @property
    def is_yet_to_begin(self):
        """
        Return whether the period is yet to begin
        :return: True if the start date is later than today, False otherwise
        """

        today = datetime.date.today()
        return self.start_date > today

    @property
    def has_already_ended(self):
        """
        Return whether the period has already over
        :return: True if today is later than the end date, False otherwise
        """

        today = datetime.date.today()
        if self.end_date is not None:
            return self.end_date < today
        else:
            return False

    @property
    def active_status(self):
        """
        Return a flag from ActiveStatus denoting the instance's active status
        :return: a flag from ActiveStatus denoting the instance's active status
        """

        if self.is_active:
            return ActiveStatus.IS_ACTIVE
        elif self.has_already_ended:
            return ActiveStatus.HAS_BEEN_ACTIVE
        elif self.is_yet_to_begin:
            return ActiveStatus.WILL_BE_ACTIVE

    @property
    def start_year(self):
        """
        Return the year of the start date
        :return: the year of the start date
        """

        return self.start_date.year

    @property
    def end_year(self):
        """
        Return the year of the end date
        :return: the year of the end date
        """

        if self.has_already_ended:
            return self.end_date.year
        else:
            raise ValueError('Period has not ended')

    @property
    def duration(self):
        """
        Return the duration of the period
        :return: the duration of the period
        """

        end_date = self.end_date or datetime.date.today()
        difference = relativedelta(end_date, self.start_date)

        period_duration = {
            'years': difference.years,
            'months': difference.months,
            'days': difference.days,
        }
        return period_duration

class BlurryPeriodMixin(PeriodMixin):
    """
    This class extends period mixin allowing the user to skip entering the date,
    which is then submitted as 1
    """

    is_full_date = models.BooleanField(
        default=False,
    )

    @property
    def duration(self):
        """
        Return duration of the period after omitting days
        :return: duration of the period after omitting days
        """

        period_duration = super().duration
        if not self.is_full_date:
            del period_duration['days']
        return period_duration

    class Meta:
        """
        Meta class for BlurryPeriodMixin
        """

        abstract = True
