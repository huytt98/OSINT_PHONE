import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from folium import plugins
import os
import json
from datetime import datetime, timedelta

class LocationTracker:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="phone_scanner")
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)
        self.cache_file = os.path.join(os.path.dirname(__file__), "cache", "location_cache.json")
        self.cache_duration = timedelta(days=7)
        self._init_cache()

    def _init_cache(self):
        """Initialize cache directory and file"""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, 'w') as f:
                json.dump({}, f)

    def _get_cached_location(self, phone_number):
        """Get cached location data if available and not expired"""
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
                if phone_number in cache:
                    cached_time = datetime.fromisoformat(cache[phone_number]['timestamp'])
                    if datetime.now() - cached_time < self.cache_duration:
                        return cache[phone_number]['data']
        except Exception:
            pass
        return None

    def _cache_location(self, phone_number, location_data):
        """Cache location data"""
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
            cache[phone_number] = {
                'timestamp': datetime.now().isoformat(),
                'data': location_data
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f)
        except Exception as e:
            print(f"Cache error: {e}")

    def get_location_info(self, phone_number):
        """Get detailed location information for a phone number."""
        # Check cache first
        if cached_data := self._get_cached_location(phone_number):
            return cached_data

        try:
            parsed_number = phonenumbers.parse(phone_number)
            country = geocoder.description_for_number(parsed_number, "en")
            carrier_name = carrier.name_for_number(parsed_number, "en")
            regions = timezone.time_zones_for_number(parsed_number)
            
            # Get more detailed location using carrier info
            search_query = f"{carrier_name}, {country}" if carrier_name else country
            location = self.geocode(search_query)
            
            if location:
                result = {
                    "country": country,
                    "carrier": carrier_name,
                    "city": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "regions": regions,
                    "map_file": self._generate_map(location),
                    "approximate": True,
                    "timestamp": datetime.now().isoformat()
                }
                self._cache_location(phone_number, result)
                return result
            return None
        except Exception as e:
            print(f"Error getting location: {e}")
            return None

    def _generate_map(self, location):
        """Generate an enhanced map with the location marker."""
        try:
            # Create map with more features
            map_obj = folium.Map(
                location=[location.latitude, location.longitude],
                zoom_start=10,
                tiles='OpenStreetMap'
            )
            
            # Add enhanced marker cluster
            marker_cluster = plugins.MarkerCluster().add_to(map_obj)
            
            # Add main marker with popup
            folium.Marker(
                [location.latitude, location.longitude],
                popup=folium.Popup(location.address, max_width=300),
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(marker_cluster)
            
            # Add circle radius for approximate area
            folium.Circle(
                radius=20000,  # 20km radius
                location=[location.latitude, location.longitude],
                color="red",
                fill=True,
                popup="Approximate Area"
            ).add_to(map_obj)
            
            # Add additional map layers
            folium.TileLayer('cartodbpositron').add_to(map_obj)
            folium.LayerControl().add_to(map_obj)
            
            # Add fullscreen option
            plugins.Fullscreen().add_to(map_obj)
            
            # Save map
            maps_dir = os.path.join(os.path.dirname(__file__), "maps")
            os.makedirs(maps_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            map_file = os.path.join(maps_dir, f"location_{timestamp}.html")
            map_obj.save(map_file)
            
            return map_file
        except Exception as e:
            print(f"Error generating map: {e}")
            return None
