import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  FormControlLabel,
  Switch,
  Alert
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { uk } from 'date-fns/locale';
import { format } from 'date-fns';
import api from '../../api/axios';
import RoutePointsList from '../../components/RoutePointsList';

const CreateTripPage = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    start_date: null,
    end_date: null,
    budget: '',
    is_public: false,
    route_points: [
      { city: '', transportation_type: '' },
      { city: '', transportation_type: '' }
    ]
  });

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

  const handleRoutePointsChange = (newPoints) => {
    setFormData(prev => ({
      ...prev,
      route_points: newPoints
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

    // Validate route points
    if (formData.route_points.length < 2) {
      errors.push('Потрібно вказати принаймні дві точки маршруту');
    }

    const invalidPoints = formData.route_points.filter(point => !point.city);
    if (invalidPoints.length > 0) {
      errors.push('Всі міста в маршруті повинні бути заповнені');
    }

    const invalidTransportation = formData.route_points
      .slice(1)  // Check all points except the first one
      .filter(point => !point.transportation_type);
    if (invalidTransportation.length > 0) {
      errors.push('Потрібно вказати тип транспорту між усіма містами');
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
        route_points: formData.route_points.map(point => ({
          ...point,
          city: point.city.trim()
        }))
      };

      const response = await api.post('/trips', formattedData);
      navigate(`/trips/${response.data.id}`);
    } catch (error) {
      console.error('Error creating trip:', error);
      if (error.response?.data?.message) {
        setError(error.response.data.message);
      } else if (error.response?.data?.error) {
        setError(error.response.data.error);
      } else {
        setError('Помилка при створенні подорожі. Перевірте введені дані.');
      }
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Створення нової подорожі
        </Typography>

        <Paper elevation={3} sx={{ p: 4 }}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Назва подорожі"
              name="title"
              value={formData.title}
              onChange={handleChange}
              margin="normal"
              required
              error={formData.title.trim() === ''}
              helperText={formData.title.trim() === '' ? 'Назва подорожі обов\'язкова' : ''}
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

            <Box sx={{ my: 3 }}>
              <RoutePointsList
                points={formData.route_points}
                onChange={handleRoutePointsChange}
              />
            </Box>

            <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={uk}>
              <Box sx={{ mt: 2, mb: 2 }}>
                <DatePicker
                  label="Дата початку"
                  value={formData.start_date}
                  onChange={handleDateChange('start_date')}
                  slotProps={{ 
                    textField: { 
                      fullWidth: true,
                      required: true,
                      error: !formData.start_date,
                      helperText: !formData.start_date ? 'Дата початку обов\'язкова' : ''
                    } 
                  }}
                />
              </Box>

              <Box sx={{ mt: 2, mb: 2 }}>
                <DatePicker
                  label="Дата завершення"
                  value={formData.end_date}
                  onChange={handleDateChange('end_date')}
                  slotProps={{ 
                    textField: { 
                      fullWidth: true,
                      required: true,
                      error: !formData.end_date || (formData.start_date && formData.end_date && formData.start_date > formData.end_date),
                      helperText: !formData.end_date ? 'Дата завершення обов\'язкова' : 
                                (formData.start_date && formData.end_date && formData.start_date > formData.end_date) ? 
                                'Дата завершення не може бути раніше дати початку' : ''
                    } 
                  }}
                  minDate={formData.start_date}
                />
              </Box>
            </LocalizationProvider>

            <TextField
              fullWidth
              label="Бюджет (грн)"
              name="budget"
              type="number"
              value={formData.budget}
              onChange={handleChange}
              margin="normal"
              inputProps={{ min: 0 }}
              error={formData.budget && (isNaN(formData.budget) || Number(formData.budget) < 0)}
              helperText={formData.budget && (isNaN(formData.budget) || Number(formData.budget) < 0) ? 
                         'Бюджет має бути додатнім числом' : ''}
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
            />

            <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                size="large"
              >
                Створити подорож
              </Button>
              <Button
                variant="outlined"
                onClick={() => navigate(-1)}
                size="large"
              >
                Скасувати
              </Button>
            </Box>
          </form>
        </Paper>
      </Box>
    </Container>
  );
};

export default CreateTripPage; 