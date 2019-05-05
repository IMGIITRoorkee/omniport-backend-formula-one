from rest_framework import response, views


class Hello(views.APIView):
    """
    This view shows a placeholder message "Hello X!"
    """

    @staticmethod
    def hello(recipient):
        """
        Return a 'Hello X!' message in JSON format
        :param recipient: the entity to say hello to
        :return: a 'Hello X!' message in JSON format
        """

        response_dict = {
            'message': f'Hello {recipient}!',
        }
        return response.Response(response_dict)

    def get(self, request, *args, **kwargs):
        """
        Return a 'Hello World!' message in JSON format
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        return Hello.hello('World')

    def post(self, request, *args, **kwargs):
        """
        Return a 'Hello X!' message in JSON format
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        recipient = request.data.get('recipient', 'World')
        return Hello.hello(recipient)
