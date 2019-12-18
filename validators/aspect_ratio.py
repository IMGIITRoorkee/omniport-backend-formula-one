from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.deconstruct import deconstructible


@deconstructible
class AspectRatioValidator:
    """
    This validator checks if the given file has an aspect ratio acceptable to
    the field
    """

    def __init__(self, aspect_ratio, tolerance=0):
        """
        Initialise a callable instance of the class with the given parameters
        :param aspect_ratio: the ratio of the width of the image to its height
        """

        self.aspect_ratio = aspect_ratio
        self.tolerance = tolerance

    def check(self, value, tolerance):
        """
        Check if the value meets all required criteria
        :param value: the value of the field
        :return: True if the value meets the criteria, False otherwise
        """

        width, height = get_image_dimensions(value)
        aspect_ratio = width / height
        return aspect_ratio >= self.aspect_ratio - self.tolerance and \
            aspect_ratio <= self.aspect_ratio + self.tolerance

    def __call__(self, value, tolerance=0):
        """
        Call the check() function and raise an error if validation fails
        :param value: the value of the field being validated
        :raise: ValidationError, if the aspect ratio is incorrect
        """

        if not self.check(value, tolerance):
            raise ValidationError(
                'The aspect ratio of the uploaded file is incorrect. '
                f'The aspect ratio should be {self.aspect_ratio}.'
            )
