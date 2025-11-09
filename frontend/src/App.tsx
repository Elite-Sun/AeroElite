import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from './store';

// Pages
import HomePage from './pages/HomePage';
import DesignPage from './pages/DesignPage';
import AssemblyPage from './pages/AssemblyPage';
import DatasetsPage from './pages/DatasetsPage';
import ProfilePage from './pages/ProfilePage';
import LoginPage from './pages/LoginPage';

// Components
import Navbar from './components/Navbar';

function App() {
  const themeMode = useSelector((state: RootState) => state.ui.theme);

  const theme = createTheme({
    palette: {
      mode: themeMode,
      primary: {
        main: '#1976d2',
      },
      secondary: {
        main: '#dc004e',
      },
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
          <Navbar />
          <main style={{ flex: 1, overflow: 'auto' }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/design" element={<DesignPage />} />
              <Route path="/design/:id" element={<DesignPage />} />
              <Route path="/assembly" element={<AssemblyPage />} />
              <Route path="/datasets" element={<DatasetsPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
