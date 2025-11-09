import React from 'react';
import {
  Container,
  Typography,
  Button,
  Box,
  Grid,
  Card,
  CardContent,
  CardActions,
  Paper,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Add, ViewInAr, Dns, Cloud } from '@mui/icons-material';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <ViewInAr fontSize="large" />,
      title: 'AI-Powered CAD Generation',
      description: 'Transform natural language prompts into fully parametric 3D aircraft models',
    },
    {
      icon: <Dns fontSize="large" />,
      title: 'Assembly System',
      description: 'Automatic alignment, fit checking, and interference detection',
    },
    {
      icon: <Cloud fontSize="large" />,
      title: 'Cloud Learning',
      description: 'Continuous learning from 27,714+ aircraft designs and user contributions',
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 8 }}>
      {/* Hero Section */}
      <Box textAlign="center" mb={8}>
        <Typography variant="h2" component="h1" gutterBottom fontWeight="bold">
          Welcome to Aero Elite
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          AI-Assisted 3D Aircraft Design System
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph sx={{ maxWidth: 800, mx: 'auto' }}>
          Design aircraft components using natural language. Our AI converts your prompts into
          fully editable, parametric CAD models with physics validation and assembly checking.
        </Typography>
        <Box mt={4}>
          <Button
            variant="contained"
            size="large"
            startIcon={<Add />}
            onClick={() => navigate('/design')}
            sx={{ mr: 2 }}
          >
            Create New Design
          </Button>
          <Button
            variant="outlined"
            size="large"
            onClick={() => navigate('/datasets')}
          >
            Explore Datasets
          </Button>
        </Box>
      </Box>

      {/* Features */}
      <Grid container spacing={4} mb={8}>
        {features.map((feature, index) => (
          <Grid item xs={12} md={4} key={index}>
            <Card elevation={3} sx={{ height: '100%' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Box color="primary.main" mb={2}>
                  {feature.icon}
                </Box>
                <Typography variant="h6" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Quick Stats */}
      <Paper elevation={2} sx={{ p: 4, textAlign: 'center' }}>
        <Grid container spacing={4}>
          <Grid item xs={12} sm={4}>
            <Typography variant="h3" color="primary" fontWeight="bold">
              27,714+
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Aircraft Designs
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h3" color="primary" fontWeight="bold">
              19,164+
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Airfoil Profiles
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h3" color="primary" fontWeight="bold">
              100%
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Parametric Models
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      {/* How It Works */}
      <Box mt={8}>
        <Typography variant="h4" gutterBottom textAlign="center" fontWeight="bold">
          How It Works
        </Typography>
        <Grid container spacing={3} mt={2}>
          {[
            { step: 1, title: 'Describe Your Design', text: 'Use natural language to describe aircraft components' },
            { step: 2, title: 'AI Generates CAD', text: 'Our AI creates parametric 3D models with physics validation' },
            { step: 3, title: 'Edit & Refine', text: 'Fine-tune parameters and geometry in our 3D editor' },
            { step: 4, title: 'Export & Share', text: 'Download in STEP, IGES, or STL formats' },
          ].map((item) => (
            <Grid item xs={12} sm={6} md={3} key={item.step}>
              <Card variant="outlined">
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h3" color="primary" fontWeight="bold">
                    {item.step}
                  </Typography>
                  <Typography variant="h6" gutterBottom>
                    {item.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {item.text}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
};

export default HomePage;
