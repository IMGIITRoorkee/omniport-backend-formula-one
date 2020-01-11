import json

from functools import wraps
from rest_framework.exceptions import NotFound
from django_redis import get_redis_connection
from django.utils.crypto import get_random_string
import swapper

from emails.actions import email_push

Person = swapper.load_model('kernel', 'Person')
CLIENT = get_redis_connection('verification')


def push(token, user_id, token_type):
    """
    This function pushes the password recovery token to
    the redis database specified.
    :param token: the token to be pushed
    :param user_id: id of user whose password is to be changed
    :param token_type: token type to be pushed
    :return: The result of push
    """

    value = json.dumps({
        'token_type': token_type,
        'user_id': user_id,
    })
    res = CLIENT.set(
        name=token,
        value=value,
        ex=3600,
        nx=True,
    )

    return res


def retrieve(token):
    """
    This function retrieves the user associated with the recovery token
    from the redis database.
    :param token: Recovery token to be parsed
    :return: The user associated with the access token
    """

    res = CLIENT.get(token)
    try:
        token_data = json.loads(res.decode('utf-8'))
    except (TypeError, AttributeError):
        return None

    return token_data


def delete(token):
    """
    This function deletes the given recovery token from the database.
    :param token: Recovery token to be deleted
    :return: error or success message
    """

    return CLIENT.delete(token)


def send_token(
        user_id,
        token_type,
        category,
        email_body,
        email_subject,
        url,
        *args,
        **kwargs
):
    """
    This function create a verification token of the given token_type and
    send an email to the concerned person.
    :param user_id: user id associated with verification token
    :param token_type: token type to be created
    :param category: category from which email is to be sent
    :param email_body: body of the email
    :param email_subject: subject of the email
    :param url: url to be included in the email body
    :return: recovery token created
    """

    use_primary_email = kwargs.get('use_primary_email', False)
    check_if_primary_email_verified = kwargs.get(
        'check_if_primary_email_verified',
        True
    )
    target_app_name = kwargs.get('target_app_name', None)
    target_app_url = kwargs.get('target_app_url', None)

    while True:
        recovery_token = get_random_string(length=20)
        existing = retrieve(recovery_token)
        if existing is None:
            push(recovery_token, user_id, token_type)
            break

    url = url.replace(token_type, recovery_token)
    email_body = email_body.replace('url', url)

    email_push(
        body_text=email_body,
        subject_text=email_subject,
        category=category,
        has_custom_user_target=True,
        persons=[Person.objects.get(user__id=user_id).id],
        use_primary_email=use_primary_email,
        check_if_primary_email_verified=check_if_primary_email_verified,
        target_app_name=target_app_name,
        target_app_url=target_app_url
    )

    return recovery_token


def verify_access_token(func):
    """
    This decorator verifies if a token exists and sends token data to view
    if it does exist.
    :param func: function to be decorated
    :return: wrapper function around the decorated function
    """

    @wraps(func)
    def wrapper(self, request):
        if request.method == 'GET':
            token = request.GET.get('token', None)
        elif request.method == 'POST':
            token = request.data.get('token', None)
        else:
            return NotFound

        if token is not None:
            token_data = retrieve(token)
        else:
            raise NotFound

        if not token_data:
            raise NotFound

        return func(self, request, token_data, token)

    return wrapper
