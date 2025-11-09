import React from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  Box,
  Avatar,
  Chip,
  Divider,
} from '@mui/material';
import { Person, Storage, Public, Lock } from '@mui/icons-material';

const ProfilePage: React.FC = () => {
  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box display="flex" alignItems="center" mb={3}>
          <Avatar sx={{ width: 80, height: 80, mr: 3 }}>
            <Person fontSize="large" />
          </Avatar>
          <Box>
            <Typography variant="h5" fontWeight="bold">
              User Profile
            </Typography>
            <Typography variant="body2" color="text.secondary">
              user@example.com
            </Typography>
            <Chip label="Free Plan" size="small" sx={{ mt: 1 }} />
          </Box>
        </Box>

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          Usage Statistics
        </Typography>

        <Grid container spacing={2} mt={1}>
          <Grid item xs={12} sm={6}>
            <Paper variant="outlined" sx={{ p: 2 }}>
              <Box display="flex" alignItems="center">
                <Storage sx={{ mr: 1, color: 'primary.main' }} />
                <Box>
                  <Typography variant="h6">0 MB</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Storage Used
                  </Typography>
                </Box>
              </Box>
            </Paper>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Paper variant="outlined" sx={{ p: 2 }}>
              <Box display="flex" alignItems="center">
                <Public sx={{ mr: 1, color: 'success.main' }} />
                <Box>
                  <Typography variant="h6">0</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Public Designs
                  </Typography>
                </Box>
              </Box>
            </Paper>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Paper variant="outlined" sx={{ p: 2 }}>
              <Box display="flex" alignItems="center">
                <Lock sx={{ mr: 1, color: 'warning.main' }} />
                <Box>
                  <Typography variant="h6">0</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Private Designs
                  </Typography>
                </Box>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default ProfilePage;
