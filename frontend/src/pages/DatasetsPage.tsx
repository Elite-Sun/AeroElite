import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
} from '@mui/material';
import { Download, CloudDownload } from '@mui/icons-material';
import axios from 'axios';

const DatasetsPage: React.FC = () => {
  const [datasets, setDatasets] = useState<any>(null);

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/datasets/list');
      setDatasets(response.data);
    } catch (error) {
      console.error('Error fetching datasets:', error);
    }
  };

  const datasetInfo = [
    {
      name: 'AircraftVerse',
      description: 'Large-scale dataset with 27,714 aircraft designs',
      entries: 27714,
      status: 'Available',
    },
    {
      name: 'G2Aero',
      description: 'Airfoil profile database with 19,164 profiles',
      entries: 19164,
      status: 'Available',
    },
    {
      name: 'NASA CRM',
      description: 'Common Research Model with validated geometry',
      entries: 1,
      status: 'Available',
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Aircraft Design Datasets
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Access curated datasets to train and improve AI models
      </Typography>

      <Grid container spacing={3} mt={2}>
        {datasetInfo.map((dataset, index) => (
          <Grid item xs={12} md={4} key={index}>
            <Card elevation={3}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {dataset.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {dataset.description}
                </Typography>
                <Chip
                  label={`${dataset.entries.toLocaleString()} entries`}
                  color="primary"
                  size="small"
                  sx={{ mb: 2 }}
                />
                <br />
                <Chip
                  label={dataset.status}
                  color="success"
                  size="small"
                  sx={{ mb: 2 }}
                />
                <br />
                <Button
                  variant="outlined"
                  startIcon={<Download />}
                  fullWidth
                  sx={{ mt: 1 }}
                >
                  Download Metadata
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default DatasetsPage;
