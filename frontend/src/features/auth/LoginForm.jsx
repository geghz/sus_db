import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import {
  Container, Box, Typography,
  TextField, Button, Checkbox, FormControlLabel
} from '@mui/material';
import { useAuth } from '../../hooks/useAuth';

const schema = yup.object({
  login: yup.string().required('Введите логин или e-mail'),
  password: yup.string().required('Введите пароль'),
});

export default function LoginForm() {
  const { login } = useAuth();
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: { remember: false },
  });

  const onSubmit = async data => {
    setError('');
    try {
      await login({
        login: data.login,
        password: data.password,
        remember: data.remember,
      });
      // редирект внутри login()
    } catch (e) {
      setError('Неверный логин или пароль');
    }
  };

  return (
    <Container maxWidth="xs">
      <Box sx={{ mt: 8, p: 3, boxShadow: 1, borderRadius: 1 }}>
        <Typography variant="h5" gutterBottom>Вход</Typography>
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <TextField
            label="Логин или Email"
            fullWidth margin="normal"
            {...register('login')}
            error={!!errors.login}
            helperText={errors.login?.message}
          />
          <TextField
            label="Пароль"
            type="password"
            fullWidth margin="normal"
            {...register('password')}
            error={!!errors.password}
            helperText={errors.password?.message}
          />
          <FormControlLabel
            control={<Checkbox {...register('remember')} />}
            label="Запомнить меня"
          />
          {error && <Typography color="error">{error}</Typography>}
          <Button
            type="submit"
            variant="contained"
            fullWidth
            sx={{ mt: 2 }}
            disabled={isSubmitting}
          >
            Войти
          </Button>
        </form>
      </Box>
    </Container>
  );
}
