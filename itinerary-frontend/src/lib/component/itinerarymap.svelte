<script>
  import { onMount } from 'svelte';
  import 'leaflet/dist/leaflet.css';

  export let llm_result;
  let map;
  let markers = [];
  let currentMapStyle = 'streets';
  let showLabels = true;
  let showRoutes = true;

  const mapStyles = {
      streets: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      satellite: 'https://server.arcgisonline.com/ArcGIS/rest/MapServer/World_Imagery/tile/{z}/{y}/{x}',
      dark: 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
      light: 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png'
  };

  const getColor = (index) => {
    const colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33F6', '#F6FF33'];
    return colors[index % colors.length];
  };

  let mapLayers = {
      base: null,
      routes: new Map(),
      markers: new Map()
  };

  function updateMapStyle(style) {
      currentMapStyle = style;
      if (map && mapLayers.base) {
          map.removeLayer(mapLayers.base);
          mapLayers.base = L.tileLayer(mapStyles[style], {
              attribution: '© OpenStreetMap contributors',
              maxZoom: 19
          }).addTo(map);
      }
  }

  function toggleLabels() {
      showLabels = !showLabels;
      markers.forEach(marker => {
          const icon = marker.getIcon();
          icon.options.html = createMarkerHtml(marker.dayIndex, marker.scheduleIndex, marker.dayColor);
          marker.setIcon(icon);
      });
  }

  function toggleRoutes() {
      showRoutes = !showRoutes;
      mapLayers.routes.forEach((route) => {
          if (showRoutes) {
              route.addTo(map);
          } else {
              route.remove();
          }
      });
  }

  function createMarkerHtml(dayIndex, scheduleIndex, color) {
      return `
          <div class="marker-container">
              <div style="background-color: ${color}; width: 30px; height: 30px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                  ${showLabels ? `<div class="marker-label">${scheduleIndex + 1}</div>` : ''}
              </div>
              ${showLabels ? `<div class="marker-day">Day ${dayIndex + 1}</div>` : ''}
          </div>
      `;
  }

  onMount(async () => {
    const L = await import('leaflet');
    
    map = L.map('map', {
      zoomControl: true,
      scrollWheelZoom: true
    }).setView([-6.2088, 106.8456], 11); // Jakarta coordinates

    mapLayers.base = L.tileLayer(mapStyles[currentMapStyle], {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map);

    llm_result.result.forEach((day, dayIndex) => {
      const dayColor = getColor(dayIndex);
      const dayCoordinates = [];

      day.schedule.forEach((item, scheduleIndex) => {
        const lat = item.longitude; // switched
        const lng = item.latitude;  // switched
        
        if (lat && lng) {
          const marker = L.marker([lat, lng], {
            icon: L.divIcon({
              html: createMarkerHtml(dayIndex, scheduleIndex, dayColor),
              className: 'custom-marker',
              iconSize: [30, 30],
              iconAnchor: [15, 15]
            })
          });

          marker.dayIndex = dayIndex;
          marker.scheduleIndex = scheduleIndex;
          marker.dayColor = dayColor;

          const popupContent = `
            <div class="p-4">
              <div class="flex items-center justify-between mb-2">
                <span class="bg-orange-100 text-orange-800 text-xs font-medium px-2 py-1 rounded">
                    Day ${dayIndex + 1} - ${item.time}
                </span>
                ${item.ratings ? `
                    <div class="flex items-center bg-yellow-100 px-2 py-1 rounded">
                        <span class="text-yellow-500">★</span>
                        <span class="ml-1 text-sm">${item.ratings}</span>
                    </div>
                ` : ''}
              </div>
              <h3 class="font-bold text-lg text-gray-800 mb-1">${item.activity}</h3>
              <div class="flex items-center text-gray-600 mb-2">
                <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                </svg>
                <span>${item.location}</span>
              </div>
              ${item.description ? `
                <p class="text-sm text-gray-600 bg-gray-50 p-2 rounded-lg mt-2">
                    ${item.description}
                </p>
              ` : ''}
              ${item.place_id ? `
                <div class="mt-2 text-xs text-gray-500">
                    Place ID: ${item.place_id}
                </div>
              ` : ''}
            </div>
          `;

          marker.bindPopup(popupContent, {
            className: 'custom-popup',
            maxWidth: 300,
            minWidth: 250
          });
          
          marker.addTo(map);
          markers.push(marker);
          dayCoordinates.push([lat, lng]);
        }
      });

      if (dayCoordinates.length > 1) {
          const route = L.polyline(dayCoordinates, {
              color: dayColor,
              weight: 3,
              opacity: 0.7,
              dashArray: '10, 10'
          });
          
          if (showRoutes) {
              route.addTo(map);
          }
          mapLayers.routes.set(dayIndex, route);
      }
    });

    if (markers.length > 0) {
      const group = L.featureGroup(markers);
      map.fitBounds(group.getBounds().pad(0.1));
    }

    L.control.scale().addTo(map);
  });
</script>

<!-- Map Controls -->
<div class="absolute right-[4rem] top-[51rem] flex flex-col gap-2 z-10">
  <div class="bg-white rounded-lg shadow-lg p-2">
      <select 
          class="w-full p-2 text-sm rounded border"
          bind:value={currentMapStyle}
          on:change={() => updateMapStyle(currentMapStyle)}
      >
          <option value="streets">Street Map</option>
          <option value="satellite">Satellite</option>
          <option value="dark">Dark Mode</option>
          <option value="light">Light Mode</option>
      </select>
  </div>
  
  <div class="bg-white rounded-lg shadow-lg p-2 flex flex-col gap-2">
      <button 
          class="px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          on:click={toggleLabels}
      >
          {showLabels ? 'Hide Labels' : 'Show Labels'}
      </button>
      <button 
          class="px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          on:click={toggleRoutes}
      >
          {showRoutes ? 'Hide Routes' : 'Show Routes'}
      </button>
  </div>
</div>

<div id="map" class="w-full h-full rounded-xl z-0"></div>

<style>
  :global(.leaflet-container) {
    height: 100%;
    width: 100%;
    border-radius: 0.75rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }

  :global(.custom-marker) {
    background: transparent;
    border: none;
  }

  :global(.marker-container) {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }

  :global(.marker-label) {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 12px;
    font-weight: bold;
    text-shadow: 0 0 2px rgba(0,0,0,0.5);
  }

  :global(.marker-day) {
    background-color: rgba(0, 0, 0, 0.75);
    color: white;
    padding: 2px 4px;
    border-radius: 4px;
    font-size: 10px;
    white-space: nowrap;
    margin-top: -4px;
  }

  :global(.custom-popup .leaflet-popup-content-wrapper) {
    border-radius: 0.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }

  :global(.custom-popup .leaflet-popup-content) {
    margin: 0;
  }

  :global(.custom-popup .leaflet-popup-close-button) {
    padding: 8px !important;
  }

  :global(.leaflet-control-zoom) {
    border-radius: 8px;
    overflow: hidden;
  }

  :global(.leaflet-control-zoom a) {
    background-color: white !important;
    color: #374151 !important;
  }

  :global(.leaflet-control-zoom a:hover) {
    background-color: #f3f4f6 !important;
  }
</style>
