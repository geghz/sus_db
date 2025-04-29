# dashboard/serializers.py
from rest_framework import serializers

class ExpiringDocSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    employee_name = serializers.CharField()
    document_name = serializers.CharField()
    version_id = serializers.IntegerField()
    expires = serializers.DateField()

class DashboardSerializer(serializers.Serializer):
    total_employees = serializers.IntegerField()
    expiring_documents = ExpiringDocSerializer(many=True)
    unread_notifications = serializers.IntegerField()
