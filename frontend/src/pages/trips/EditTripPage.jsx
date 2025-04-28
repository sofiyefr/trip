import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  FormControlLabel,
  Switch,
  Alert,
  CircularProgress
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { uk } from 'date-fns/locale';
import { format, parse } from 'date-fns';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import RoutePointsList from '../../components/RoutePointsList';
import api from '../../api/axios';

const EditTripPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    start_date: null,
    end_date: null,
    budget: '',
    is_public: false,
    route_points: []
  });

  useEffect(() => {
    fetchTripDetails();
  }, [id]);

  const fetchTripDetails = async () => {
    try {
      const response = await api.get(`/trips/${id}`);
      const trip = response.data;
      
      setFormData({
        title: trip.title,
        description: trip.description || '',
        start_date: parse(trip.start_date, 'yyyy-MM-dd', new Date()),
        end_date: parse(trip.end_date, 'yyyy-MM-dd', new Date()),
        budget: trip.budget.toString(),
        is_public: trip.is_public,
        route_points: trip.route_points || []
      });
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

  const handleChange = (e) => {
    const { name, value, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'is_public' ? checked : value
    }));
  };

  const handleDateChange = (field) => (date) => {
    setFormData(prev => ({
      ...prev,
      [field]: date
    }));
  };

  const handleRoutePointsChange = (newRoutePoints) => {
    setFormData(prev => ({
      ...prev,
      route_points: newRoutePoints
    }));
  };

  const validateForm = () => {
    const errors = [];
    
    if (!formData.title.trim()) {
      errors.push('Назва подорожі обов\'язкова');
    }
    
    if (!formData.start_date) {
      errors.push('Дата початку обов\'язкова');
    }
    
    if (!formData.end_date) {
      errors.push('Дата завершення обов\'язкова');
    }
    
    if (formData.start_date && formData.end_date && formData.start_date > formData.end_date) {
      errors.push('Дата завершення не може бути раніше дати початку');
    }
    
    if (formData.budget && (isNaN(formData.budget) || Number(formData.budget) < 0)) {
      errors.push('Бюджет має бути додатнім числом');
    }

    if (!formData.route_points || formData.route_points.length < 2) {
      errors.push('Додайте хоча б два пункти маршруту');
    }

    const hasInvalidRoutePoints = formData.route_points.some(
      point => !point.city || !point.transportation_type
    );
    if (hasInvalidRoutePoints) {
      errors.push('Заповніть всі дані для кожного пункту маршруту');
    }
    
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const validationErrors = validateForm();
    if (validationErrors.length > 0) {
      setError(validationErrors.join('. '));
      return;
    }

    try {
      const formattedData = {
        ...formData,
        title: formData.title.trim(),
        description: formData.description.trim(),
        start_date: formData.start_date ? format(formData.start_date, 'yyyy-MM-dd') : null,
        end_date: formData.end_date ? format(formData.end_date, 'yyyy-MM-dd') : null,
        budget: formData.budget ? Number(formData.budget) : 0,
        route_points: formData.route_points.map((point, index) => ({
          ...point,
          order_number: index
        }))
      };

      await api.put(`/trips/${id}`, formattedData);
      navigate(`/trips/${id}`);
    } catch (error) {
      console.error('Error updating trip:', error);
      if (error.response?.data?.message) {
        setError(error.response.data.message);
      } else if (error.response?.data?.error) {
        setError(error.response.data.error);
      } else {
        setError('Помилка при оновленні подорожі. Перевірте введені дані.');
      }
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error && !formData.title) {
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

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" alignItems="center" mb={3}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate(`/trips/${id}`)}
            sx={{ mr: 2 }}
          >
            Назад
          </Button>
          <Typography variant="h4" component="h1">
            Редагування подорожі
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Paper sx={{ p: 3 }}>
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Назва подорожі"
              name="title"
              value={formData.title}
              onChange={handleChange}
              margin="normal"
              required
            />

            <TextField
              fullWidth
              label="Опис"
              name="description"
              value={formData.description}
              onChange={handleChange}
              margin="normal"
              multiline
              rows={4}
            />

            <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={uk}>
              <Box sx={{ mt: 2, mb: 2 }}>
                <DatePicker
                  label="Дата початку"
                  value={formData.start_date}
                  onChange={handleDateChange('start_date')}
                  renderInput={(params) => <TextField {...params} fullWidth sx={{ mr: 2 }} />}
                />
              </Box>
              <Box sx={{ mt: 2, mb: 2 }}>
                <DatePicker
                  label="Дата завершення"
                  value={formData.end_date}
                  onChange={handleDateChange('end_date')}
                  renderInput={(params) => <TextField {...params} fullWidth />}
                />
              </Box>
            </LocalizationProvider>

            <TextField
              fullWidth
              label="Бюджет"
              name="budget"
              type="number"
              value={formData.budget}
              onChange={handleChange}
              margin="normal"
            />

            <FormControlLabel
              control={
                <Switch
                  checked={formData.is_public}
                  onChange={handleChange}
                  name="is_public"
                />
              }
              label="Публічна подорож"
              sx={{ mt: 2, mb: 2, display: 'block' }}
            />

            <Typography variant="h6" sx={{ mt: 3, mb: 2 }}>
              Маршрут подорожі
            </Typography>

            <RoutePointsList
              points={formData.route_points}
              onChange={handleRoutePointsChange}
            />

            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                size="large"
              >
                Зберегти зміни
              </Button>
            </Box>
          </form>
        </Paper>
      </Box>
    </Container>
  );
};

export default EditTripPage; 