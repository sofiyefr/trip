import React from 'react';
import {
  Box,
  TextField,
  IconButton,
  MenuItem,
  Grid,
  Typography,
  Button
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

const transportationOptions = [
  { value: 'plane', label: 'Літак' },
  { value: 'train', label: 'Потяг' },
  { value: 'bus', label: 'Автобус' },
  { value: 'car', label: 'Автомобіль' },
  { value: 'other', label: 'Інше' }
];

const RoutePointsList = ({ points, onChange }) => {
  const handleAddPoint = () => {
    onChange([...points, { city: '', transportation_type: '' }]);
  };

  const handleRemovePoint = (index) => {
    const newPoints = points.filter((_, i) => i !== index);
    onChange(newPoints);
  };

  const handlePointChange = (index, field, value) => {
    const newPoints = [...points];
    newPoints[index] = { ...newPoints[index], [field]: value };
    onChange(newPoints);
  };

  return (
    <Box>
      <Typography variant="subtitle1" gutterBottom>
        Маршрут подорожі
      </Typography>
      
      {points.map((point, index) => (
        <Box key={index} sx={{ mb: 2 }}>
          <Grid container spacing={2} alignItems="center">
            {index === 0 ? (
              // Перша точка (місто відправлення)
              <Grid item xs={12} sm={5}>
                <TextField
                  fullWidth
                  label="Місто відправлення"
                  value={point.city}
                  onChange={(e) => handlePointChange(index, 'city', e.target.value)}
                  required
                  error={!point.city}
                  helperText={!point.city ? 'Вкажіть місто' : ''}
                />
              </Grid>
            ) : (
              // Наступні точки (тип транспорту + місто)
              <>
                <Grid item xs={12} sm={5}>
                  <TextField
                    select
                    fullWidth
                    label="Тип транспорту"
                    value={point.transportation_type || ''}
                    onChange={(e) => handlePointChange(index, 'transportation_type', e.target.value)}
                    required
                    error={!point.transportation_type}
                    helperText={!point.transportation_type ? 'Виберіть тип транспорту' : ''}
                  >
                    {transportationOptions.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>
                <Grid item xs={12} sm={1} sx={{ display: 'flex', justifyContent: 'center' }}>
                  <ArrowForwardIcon color="action" />
                </Grid>
                <Grid item xs={12} sm={5}>
                  <TextField
                    fullWidth
                    label="Місто"
                    value={point.city}
                    onChange={(e) => handlePointChange(index, 'city', e.target.value)}
                    required
                    error={!point.city}
                    helperText={!point.city ? 'Вкажіть місто' : ''}
                  />
                </Grid>
              </>
            )}
            
            <Grid item xs={12} sm={1}>
              <IconButton
                color="error"
                onClick={() => handleRemovePoint(index)}
                disabled={points.length <= 2}
              >
                <DeleteIcon />
              </IconButton>
            </Grid>
          </Grid>
        </Box>
      ))}
      
      <Button
        startIcon={<AddIcon />}
        onClick={handleAddPoint}
        variant="outlined"
        sx={{ mt: 1 }}
      >
        Додати точку маршруту
      </Button>
    </Box>
  );
};

export default RoutePointsList; 