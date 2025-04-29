// src/features/admin/UserList.jsx
import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchUsers, deleteUser } from '../../api/users';
import {
  DataGrid, GridActionsCellItem
} from '@mui/x-data-grid';
import { Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

export default function UserList() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { data: resp, isLoading } = useQuery(['users'], fetchUsers);
  const del = useMutation(deleteUser, {
    onSuccess: () => queryClient.invalidateQueries(['users']),
  });

  const rows = resp?.data || [];
  const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'username', headerName: 'Username', flex: 1 },
    { field: 'email', headerName: 'Email', flex: 1 },
    { field: 'first_name', headerName: 'First Name', flex: 1 },
    { field: 'last_name', headerName: 'Last Name', flex: 1 },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 120,
      getActions: ({ id }) => [
        <GridActionsCellItem
          icon={<EditIcon />}
          label="Edit"
          onClick={() => navigate(`/admin/users/${id}`)}
        />,
        <GridActionsCellItem
          icon={<DeleteIcon />}
          label="Delete"
          onClick={() => del.mutate(id)}
        />,
      ],
    },
  ];

  return (
    <Box sx={{ height: 600, width: '100%' }}>
      <Button
        variant="contained"
        sx={{ mb: 2 }}
        onClick={() => navigate('/admin/users/new')}
      >
        Создать пользователя
      </Button>
      <DataGrid
        rows={rows}
        columns={columns}
        loading={isLoading}
        getRowId={(row) => row.id}
        autoPageSize
      />
    </Box>
  );
}
