from rest_framework import permissions
from rest_framework.views import View

from loans.models import Loan


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view: View):
        return request.user.is_authenticated


class IsColaborator(permissions.BasePermission):
    def has_permission(self, request, view: View):
        return request.user.is_authenticated and request.user.is_colaborator


class IsColaboratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view: View):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated and request.user.is_colaborator


class IsAuthenticatedOrCreate(permissions.BasePermission):
    def has_permission(self, request, view: View):
        if request.method == 'POST':
            return True
        return request.user.is_authenticated


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view: View):
        return (request.user.is_authenticated and
                request.user.is_colaborator is False)


class IsLoanOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Loan):
        return (request.user.is_authenticated and
                request.user.id == obj.user.id)
