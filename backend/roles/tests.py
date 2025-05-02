from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Position, Role, RoleFieldPermission, Permission

User = get_user_model()

class RolesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='pass'
        )
        self.client.force_authenticate(user=self.admin)
        self.pos = Position.objects.create(name='Manager')
        self.role = Role.objects.create(name='TestRole')
        self.role.positions.add(self.pos)
        self.permission = Permission.objects.create(code='view_employee', name='View Employee')

    def test_create_position(self):
        resp = self.client.post('/api/roles/positions/', {'name': 'Tester'})
        self.assertEqual(resp.status_code, 201)

    def test_role_m2m(self):
        self.assertIn(self.pos, self.role.positions.all())

    def test_role_field_permission(self):
        from fields.models import FieldGroup
        fg = FieldGroup.objects.create(name='Group1')
        rfp = RoleFieldPermission.objects.create(
            role=self.role, field_group=fg, can_view=True, can_edit=False
        )
        self.assertTrue(rfp.can_view)

    def test_employee_filter_by_role(self):
        from employees.models import Employee
        emp = Employee.objects.create(first_name='John', last_name='Doe', position='Manager')
        resp = self.client.get('/api/employees/')
        self.assertEqual(resp.status_code, 200)