import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Box,
  Switch,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Brightness4,
  Brightness7,
  Person,
  ViewInAr,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { toggleTheme, toggleSidebar } from '../store/slices/uiSlice';
import { logout } from '../store/slices/authSlice';

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const theme = useSelector((state: RootState) => state.ui.theme);
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);

  return (
    <AppBar position="static" elevation={2}>
      <Toolbar>
        <IconButton
          edge="start"
          color="inherit"
          onClick={() => dispatch(toggleSidebar())}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>

        <ViewInAr sx={{ mr: 1 }} />
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 0, fontWeight: 'bold', cursor: 'pointer' }}
          onClick={() => navigate('/')}
        >
          Aero Elite
        </Typography>
        <Typography variant="caption" sx={{ ml: 1, opacity: 0.7 }}>
          AI-Assisted Aircraft Design
        </Typography>

        <Box sx={{ flexGrow: 1 }} />

        <Button color="inherit" onClick={() => navigate('/design')}>
          Create Design
        </Button>
        <Button color="inherit" onClick={() => navigate('/assembly')}>
          Assembly
        </Button>
        <Button color="inherit" onClick={() => navigate('/datasets')}>
          Datasets
        </Button>

        <IconButton color="inherit" onClick={() => dispatch(toggleTheme())}>
          {theme === 'dark' ? <Brightness7 /> : <Brightness4 />}
        </IconButton>

        {isAuthenticated ? (
          <>
            <IconButton color="inherit" onClick={() => navigate('/profile')}>
              <Person />
            </IconButton>
            <Button
              color="inherit"
              onClick={() => {
                dispatch(logout());
                navigate('/');
              }}
            >
              Logout
            </Button>
          </>
        ) : (
          <Button color="inherit" onClick={() => navigate('/login')}>
            Login
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
