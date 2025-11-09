import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Divider,
  Link,
} from '@mui/material';
import { Google } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { loginSuccess } from '../store/slices/authSlice';
import axios from 'axios';

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      if (isRegister) {
        // Register
        await axios.post('http://localhost:8000/api/v1/auth/register', {
          email,
          username,
          password,
        });
        alert('Registration successful! Please login.');
        setIsRegister(false);
      } else {
        // Login
        const response = await axios.post('http://localhost:8000/api/v1/auth/login', {
          email,
          password,
        });

        dispatch(
          loginSuccess({
            user: { id: 1, email, username: email.split('@')[0], is_premium: false },
            token: response.data.access_token,
          })
        );
        navigate('/');
      }
    } catch (error) {
      console.error('Auth error:', error);
      alert('Authentication failed');
    }
  };

  return (
    <Container maxWidth="sm" sx={{ py: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" textAlign="center" gutterBottom fontWeight="bold">
          {isRegister ? 'Create Account' : 'Login'}
        </Typography>
        <Typography variant="body2" textAlign="center" color="text.secondary" paragraph>
          {isRegister
            ? 'Sign up to start creating aircraft designs'
            : 'Welcome back to Aero Elite'}
        </Typography>

        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          {isRegister && (
            <TextField
              fullWidth
              label="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              sx={{ mb: 2 }}
            />
          )}

          <TextField
            fullWidth
            type="email"
            label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            sx={{ mb: 2 }}
          />

          <TextField
            fullWidth
            type="password"
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            sx={{ mb: 3 }}
          />

          <Button fullWidth variant="contained" size="large" type="submit">
            {isRegister ? 'Sign Up' : 'Login'}
          </Button>

          <Divider sx={{ my: 3 }}>OR</Divider>

          <Button
            fullWidth
            variant="outlined"
            startIcon={<Google />}
            size="large"
          >
            Continue with Google
          </Button>

          <Box textAlign="center" mt={2}>
            <Link
              component="button"
              variant="body2"
              onClick={() => setIsRegister(!isRegister)}
              type="button"
            >
              {isRegister
                ? 'Already have an account? Login'
                : "Don't have an account? Sign Up"}
            </Link>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default LoginPage;
