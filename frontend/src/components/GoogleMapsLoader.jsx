import { useEffect } from 'react';

const GOOGLE_MAPS_API_KEY = 'AIzaSyBLgHpuxW8Qvi64cOQg1dynYnptuY-_ybc';

export const loadGoogleMaps = () => {
  return new Promise((resolve, reject) => {
    if (window.google) {
      resolve(window.google);
      return;
    }

    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&libraries=places`;
    script.async = true;
    script.defer = true;
    script.onload = () => resolve(window.google);
    script.onerror = (error) => reject(error);
    document.head.appendChild(script);
  });
};

const GoogleMapsLoader = ({ onLoad }) => {
  useEffect(() => {
    loadGoogleMaps()
      .then(() => {
        if (onLoad) onLoad();
      })
      .catch((error) => {
        console.error('Error loading Google Maps:', error);
      });
  }, [onLoad]);

  return null;
};

export default GoogleMapsLoader; 