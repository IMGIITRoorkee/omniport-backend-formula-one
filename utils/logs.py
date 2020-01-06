import logging


def get_logging_function(logger_name, module_name):
    """
    This function is used to create a logging function for different modules
    using the specified logger.
    :param logger_name: the logger name
    :param module_name: the module name
    :return: the logging function
    """

    logger = logging.getLogger(logger_name)

    def log(message, log_type, user=None):
        """
        Logs the message with user information
        :param message: the message to be logged
        :param log_type: type of event to be logged
        :param user: user responsible for the event
        """

        if user is not None:
            user_information = f'User: {user}({user.id}) '
        else:
            user_information = ''

        getattr(logger, log_type, 'info')(
            f'{[module_name.upper()]} '
            f'{user_information}'
            f'{message}'
        )

    return log
