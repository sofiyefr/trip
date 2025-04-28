import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../api/axios';
import { useAuth } from '../../context/AuthContext';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  Fab,
  CircularProgress,
  Alert
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';

const DashboardPage = () => {
  const navigate = useNavigate();
  const { logout, user } = useAuth();
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Verify authentication on component mount
  useEffect(() => {
    // If no user is logged in after auth context loading completes, redirect to login
    if (!localStorage.getItem('token')) {
      console.log('No token found, redirecting to login');
      navigate('/login');
      return;
    }
    
    fetchTrips();
  }, [navigate]);

  const fetchTrips = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Validate token before making request
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }
      
      const response = await api.get('/trips');
      setTrips(response.data.trips || []);
    } catch (error) {
      console.error('Error fetching trips:', error);
      
      // Handle authentication errors
      if (error.response?.status === 401 || error.response?.status === 422) {
        const errorData = error.response?.data;
        if (
          errorData?.error === 'Invalid token' || 
          errorData?.error === 'Token expired' ||
          errorData?.error === 'Authentication error' ||
          errorData?.message?.includes('Subject') ||
          errorData?.message?.includes('token')
        ) {
          setError('Сесія закінчилася. Будь ласка, увійдіть знову.');
          // Logout and redirect after a short delay
          setTimeout(() => {
            logout();
            navigate('/login');
          }, 1500);
        } else {
          setError('Помилка автентифікації. Будь ласка, увійдіть знову.');
        }
      } else if (error.message === 'No authentication token found') {
        setError('Необхідно увійти в систему');
        setTimeout(() => {
          logout();
          navigate('/login');
        }, 1500);
      } else {
        setError('Помилка при завантаженні подорожей');
      }
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('uk-UA');
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4" component="h1">
          Мої подорожі
        </Typography>
        <Fab
          color="primary"
          aria-label="add"
          onClick={() => navigate('/trips/new')}
        >
          <AddIcon />
        </Fab>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {trips && trips.length > 0 ? (
          trips.map((trip) => (
            <Grid item xs={12} sm={6} md={4} key={trip.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" component="h2" gutterBottom>
                    {trip.title}
                  </Typography>
                  <Typography color="textSecondary" gutterBottom>
                    {trip.description}
                  </Typography>
                  <Typography variant="body2" component="p">
                    Дати: {formatDate(trip.start_date)} - {formatDate(trip.end_date)}
                  </Typography>
                  <Typography variant="body2" component="p">
                    Бюджет: {trip.budget} грн
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    color="primary"
                    onClick={() => navigate(`/trips/${trip.id}`)}
                  >
                    Деталі
                  </Button>
                  <Button 
                    size="small" 
                    color="primary"
                    onClick={() => navigate(`/trips/${trip.id}/edit`)}
                  >
                    Редагувати
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))
        ) : (
          !error && (
            <Grid item xs={12}>
              <Box textAlign="center" py={4}>
                <Typography variant="h6" color="textSecondary">
                  У вас поки немає подорожей
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  sx={{ mt: 2 }}
                  onClick={() => navigate('/trips/new')}
                >
                  Створити першу подорож
                </Button>
              </Box>
            </Grid>
          )
        )}
      </Grid>
    </Container>
  );
};

export default DashboardPage; 