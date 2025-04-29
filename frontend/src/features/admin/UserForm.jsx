// src/features/admin/UserForm.jsx
import React, { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchUser, createUser, updateUser } from '../../api/users';
import {
  TextField, Button, Checkbox, FormControlLabel, Box,
  MenuItem, Select, InputLabel, FormControl
} from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';

export default function UserForm() {
  const { id } = useParams();
  const isNew = id === 'new';
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const { data } = useQuery(['user', id], () => fetchUser(id), {
    enabled: !isNew,
  });
  const createMut = useMutation(createUser, {
    onSuccess: () => {
      queryClient.invalidateQueries(['users']);
      navigate('/admin/users');
    }
  });
  const updateMut = useMutation(
    (data) => updateUser(id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['users']);
        navigate('/admin/users');
      }
    }
  );

  const { control, handleSubmit, reset } = useForm({
    defaultValues: {
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      password: '',
      roles: [],
      permissions: [],
      is_active: true,
    }
  });

  useEffect(() => {
    if (data?.data && !isNew) {
      reset(data.data);
    }
  }, [data, reset, isNew]);

  const onSubmit = (formData) => {
    if (isNew) createMut.mutate(formData);
    else updateMut.mutate(formData);
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit(onSubmit)}
      sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}
    >
      <Controller
        name="username"
        control={control}
        rules={{ required: 'Обязательное поле' }}
        render={({ field, fieldState }) => (
          <TextField
            {...field}
            label="Username"
            fullWidth
            margin="normal"
            error={!!fieldState.error}
            helperText={fieldState.error?.message}
          />
        )}
      />
      {/* Аналогично email, first_name, last_name, password */}
      <Controller
        name="is_active"
        control={control}
        render={({ field }) => (
          <FormControlLabel
            control={<Checkbox {...field} checked={field.value} />}
            label="Активен"
          />
        )}
      />
      {/* TODO: селекты для roles и permissions (fetch + MultiSelect) */}
      <Button type="submit" variant="contained" sx={{ mt: 2 }}>
        {isNew ? 'Создать' : 'Сохранить'}
      </Button>
    </Box>
  );
}
