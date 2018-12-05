from django.db.utils import IntegrityError

from rest_framework import response


class IntegrityErrorAwareMixin():
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as err:
            return response.Response({
                'error': [
                    'There is already an item by that name or ID.',
                ],
            }, status=400)
