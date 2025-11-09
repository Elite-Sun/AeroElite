import React from 'react';
import { Container, Typography, Paper } from '@mui/material';
import CADViewer3D from '../components/CADViewer3D';

const AssemblyPage: React.FC = () => {
  return (
    <Container maxWidth="xl" sx={{ py: 3, height: 'calc(100vh - 100px)' }}>
      <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
        <Typography variant="h5" gutterBottom>
          Aircraft Assembly
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          Assemble multiple components with automatic alignment and interference checking
        </Typography>
        <div style={{ height: 'calc(100% - 80px)' }}>
          <CADViewer3D />
        </div>
      </Paper>
    </Container>
  );
};

export default AssemblyPage;
