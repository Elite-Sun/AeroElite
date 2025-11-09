import React, { useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  CircularProgress,
  Alert,
} from '@mui/material';
import { Send, Download, Check } from '@mui/icons-material';
import CADViewer3D from '../components/CADViewer3D';
import axios from 'axios';

const DesignPage: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [componentType, setComponentType] = useState('wing');
  const [loading, setLoading] = useState(false);
  const [design, setDesign] = useState<any>(null);
  const [validation, setValidation] = useState<any>(null);

  const handleCreateDesign = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/v1/design/create', {
        prompt,
        component_type: componentType,
        is_public: true,
        allow_learning: true,
      });
      setDesign(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error creating design:', error);
      setLoading(false);
    }
  };

  const handleValidate = async () => {
    if (!design) return;
    try {
      const response = await axios.post(
        `http://localhost:8000/api/v1/design/${design.id}/validate`
      );
      setValidation(response.data);
    } catch (error) {
      console.error('Error validating design:', error);
    }
  };

  return (
    <Container maxWidth="xl" sx={{ py: 3, height: 'calc(100vh - 100px)' }}>
      <Grid container spacing={3} sx={{ height: '100%' }}>
        {/* Left Panel - Input */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 3, height: '100%', overflow: 'auto' }}>
            <Typography variant="h5" gutterBottom fontWeight="bold">
              Create Design
            </Typography>

            <FormControl fullWidth sx={{ mt: 2 }}>
              <InputLabel>Component Type</InputLabel>
              <Select
                value={componentType}
                label="Component Type"
                onChange={(e) => setComponentType(e.target.value)}
              >
                <MenuItem value="wing">Wing</MenuItem>
                <MenuItem value="fuselage">Fuselage</MenuItem>
                <MenuItem value="tail">Tail</MenuItem>
                <MenuItem value="engine_nacelle">Engine Nacelle</MenuItem>
                <MenuItem value="landing_gear">Landing Gear</MenuItem>
              </Select>
            </FormControl>

            <TextField
              fullWidth
              multiline
              rows={8}
              label="Design Prompt"
              placeholder="Example: Create a 25m wingspan with NACA2412 airfoil, 4° dihedral, 2.5m root chord tapering to 1.5m tip chord"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              sx={{ mt: 2 }}
            />

            <Button
              fullWidth
              variant="contained"
              size="large"
              startIcon={loading ? <CircularProgress size={20} /> : <Send />}
              onClick={handleCreateDesign}
              disabled={!prompt || loading}
              sx={{ mt: 2 }}
            >
              {loading ? 'Generating...' : 'Generate CAD Model'}
            </Button>

            {design && (
              <>
                <Box mt={3}>
                  <Alert severity="success">
                    Design created successfully!
                  </Alert>
                </Box>

                <Typography variant="h6" sx={{ mt: 3 }}>
                  Design Info
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Name: {design.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Type: {design.component_type}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Format: {design.cad_format?.toUpperCase()}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Size: {design.file_size_mb?.toFixed(2)} MB
                </Typography>

                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Check />}
                  onClick={handleValidate}
                  sx={{ mt: 2 }}
                >
                  Run Physics Validation
                </Button>

                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Download />}
                  sx={{ mt: 1 }}
                >
                  Export Model
                </Button>

                {validation && (
                  <Box mt={2}>
                    <Typography variant="h6">Validation Results</Typography>
                    {validation.valid ? (
                      <Alert severity="success">Design is valid!</Alert>
                    ) : (
                      <Alert severity="error">Validation failed</Alert>
                    )}
                    {validation.warnings?.length > 0 && (
                      <Alert severity="warning" sx={{ mt: 1 }}>
                        {validation.warnings.join(', ')}
                      </Alert>
                    )}
                  </Box>
                )}
              </>
            )}
          </Paper>
        </Grid>

        {/* Right Panel - 3D Viewer */}
        <Grid item xs={12} md={8}>
          <Paper elevation={3} sx={{ height: '100%', overflow: 'hidden' }}>
            <CADViewer3D modelData={design} />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default DesignPage;
