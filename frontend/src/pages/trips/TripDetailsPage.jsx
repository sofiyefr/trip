import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Grid,
  Divider,
  CircularProgress,
  Alert,
  IconButton
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import MapIcon from '@mui/icons-material/Map';
import { format } from 'date-fns';
import { uk } from 'date-fns/locale';
import api from '../../api/axios';
import GoogleMapsLoader from '../../components/GoogleMapsLoader';

const TripDetailsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [trip, setTrip] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);
  const [isMapLoaded, setIsMapLoaded] = useState(false);

  useEffect(() => {
    fetchTripDetails();
  }, [id]);

  useEffect(() => {
    if (trip && isMapLoaded && !map) {
      initMap();
    }
  }, [trip, isMapLoaded]);

  const initMap = () => {
    if (!mapRef.current) return;

    const newMap = new google.maps.Map(mapRef.current, {
      zoom: 4,
      center: { lat: 49.8397, lng: 24.0297 } // Львів як центральна точка
    });
    setMap(newMap);
    
    if (trip.route_points.length >= 2) {
      displayRouteOnMap(trip.route_points, newMap);
    }
  };

  const displayRouteOnMap = (points, targetMap) => {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(targetMap);

    const origin = points[0].city;
    const destination = points[points.length - 1].city;
    const waypoints = points.slice(1, -1).map(point => ({
      location: point.city,
      stopover: true
    }));

    directionsService.route({
      origin,
      destination,
      waypoints,
      travelMode: 'DRIVING'
    }, (result, status) => {
      if (status === 'OK') {
        directionsRenderer.setDirections(result);
      }
    });
  };

  const openInGoogleMaps = (fromCity, toCity, transportType) => {
    let travelMode = 'driving';
    switch (transportType) {
      case 'plane':
        travelMode = 'flights';
        break;
      case 'train':
        travelMode = 'transit';
        break;
      case 'bus':
        travelMode = 'transit';
        break;
      case 'car':
        travelMode = 'driving';
        break;
      default:
        travelMode = 'driving';
    }

    const url = `https://www.google.com/maps/dir/?api=1&origin=${encodeURIComponent(fromCity)}&destination=${encodeURIComponent(toCity)}&travelmode=${travelMode}`;
    window.open(url, '_blank');
  };

  const fetchTripDetails = async () => {
    try {
      const response = await api.get(`/trips/${id}`);
      setTrip(response.data);
      setError('');
    } catch (error) {
      console.error('Error fetching trip details:', error);
      if (error.response?.status === 404) {
        setError('Подорож не знайдена');
      } else {
        setError('Помилка при завантаженні даних подорожі');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Ви впевнені, що хочете видалити цю подорож?')) {
      return;
    }

    try {
      await api.delete(`/trips/${id}`);
      navigate('/dashboard', { replace: true });
    } catch (error) {
      console.error('Error deleting trip:', error);
      setError('Помилка при видаленні подорожі');
    }
  };

  const getTransportationLabel = (type) => {
    const types = {
      'plane': 'Літак',
      'train': 'Потяг',
      'bus': 'Автобус',
      'car': 'Автомобіль',
      'other': 'Інше'
    };
    return types[type] || type;
  };

  const renderRoute = () => {
    if (!trip.route_points || trip.route_points.length === 0) {
      return 'Маршрут не вказано';
    }

    return trip.route_points.map((point, index) => {
      if (index === trip.route_points.length - 1) return null;

      const nextPoint = trip.route_points[index + 1];
      return (
        <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 1, justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Typography variant="body1" component="span">
              {point.city}
            </Typography>
            <ArrowForwardIcon sx={{ mx: 1 }} />
            <Typography variant="body1" component="span">
              {nextPoint.city}
            </Typography>
            {nextPoint.transportation_type && (
              <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                ({getTransportationLabel(nextPoint.transportation_type)})
              </Typography>
            )}
          </Box>
          <Button
            startIcon={<MapIcon />}
            size="small"
            onClick={() => openInGoogleMaps(point.city, nextPoint.city, nextPoint.transportation_type)}
          >
            Переглянути на картах
          </Button>
        </Box>
      );
    });
  };

  const handleMapLoad = () => {
    setIsMapLoaded(true);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md">
        <Box sx={{ mt: 4 }}>
          <Alert severity="error">{error}</Alert>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/dashboard')}
            sx={{ mt: 2 }}
          >
            Повернутися до списку
          </Button>
        </Box>
      </Container>
    );
  }

  if (!trip) {
    return null;
  }

  return (
    <Container maxWidth="md">
      <GoogleMapsLoader onLoad={handleMapLoad} />
      <Box sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" alignItems="center" mb={3}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/dashboard')}
            sx={{ mr: 2 }}
          >
            Назад
          </Button>
          <Typography variant="h4" component="h1" sx={{ flexGrow: 1 }}>
            {trip.title}
          </Typography>
          <IconButton
            color="primary"
            onClick={() => navigate(`/trips/${id}/edit`)}
            sx={{ mr: 1 }}
          >
            <EditIcon />
          </IconButton>
          <IconButton color="error" onClick={handleDelete}>
            <DeleteIcon />
          </IconButton>
        </Box>

        <Paper elevation={3} sx={{ p: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Опис
              </Typography>
              <Typography variant="body1" paragraph>
                {trip.description || 'Опис відсутній'}
              </Typography>
              <Divider sx={{ my: 2 }} />
            </Grid>

            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Маршрут
              </Typography>
              <Box sx={{ mb: 2 }}>
                {renderRoute()}
              </Box>
              <Divider sx={{ my: 2 }} />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1" color="text.secondary">
                Дата початку
              </Typography>
              <Typography variant="body1">
                {format(new Date(trip.start_date), 'dd MMMM yyyy', { locale: uk })}
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1" color="text.secondary">
                Дата завершення
              </Typography>
              <Typography variant="body1">
                {format(new Date(trip.end_date), 'dd MMMM yyyy', { locale: uk })}
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1" color="text.secondary">
                Бюджет
              </Typography>
              <Typography variant="body1">
                {trip.budget.toLocaleString()} грн
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1" color="text.secondary">
                Статус
              </Typography>
              <Typography variant="body1">
                {trip.is_public ? 'Публічна подорож' : 'Приватна подорож'}
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider sx={{ my: 2 }} />
              <Typography variant="h6" gutterBottom>
                Карта маршруту
              </Typography>
              <Box
                ref={mapRef}
                sx={{
                  width: '100%',
                  height: '400px',
                  borderRadius: 1,
                  overflow: 'hidden'
                }}
              />
            </Grid>
          </Grid>
        </Paper>
      </Box>
    </Container>
  );
};

export default TripDetailsPage; 