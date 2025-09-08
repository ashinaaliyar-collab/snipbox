from rest_framework.response import Response
from rest_framework import status

class StandardResponseMixin:

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response({
                "message": "Created successfully",
                "data": response.data
            }, status=response.status_code)
        return Response({
            "error": response.data
        }, status=response.status_code)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code in [status.HTTP_200_OK, status.HTTP_202_ACCEPTED]:
            return Response({
                "message": "Updated successfully",
                "data": response.data
            }, status=response.status_code)
        return Response({
            "error": response.data
        }, status=response.status_code)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]:
            return Response({
                "message": "Deleted successfully"
            }, status=response.status_code)
        return Response({
            "error": response.data
        }, status=response.status_code)
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({
                "message": "Retrieved successfully",
                "data": response.data
            }, status=response.status_code)
        return Response({
            "error": response.data
        }, status=response.status_code)
    