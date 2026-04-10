/* ===================================================
   Orlando Explorer — Service Worker orlando-explorer-v1

   PRODUCTION: Update CACHE_NAME version on each deploy to bust all caches.
   Add Firebase Storage / Cloudflare CDN image URLs to STATIC_ASSETS as the
   app grows. Consider workbox-build or workbox-webpack-plugin for auto manifest.
   =================================================== */

const CACHE_NAME = 'orlando-explorer-v1';

// Critical app-shell resources cached on install.
// Add more asset URLs here as the app grows.
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/sw.js',
  // Google Fonts CSS (fonts themselves cached on first fetch)
  'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600;700&display=swap',
  // Leaflet map library
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
];

// Dynamic / API origins — always try network first for these
const NETWORK_FIRST_HOSTS = [
  'api.openweathermap.org',
  'nominatim.openstreetmap.org',
  'openrouteservice.org',
  'firestore.googleapis.com',
  'firebase.googleapis.com',
  'open-meteo.com',
];

/* ---- INSTALL: pre-cache critical app shell ---- */
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      // Use allSettled so a single 404 doesn't abort the entire install
      return Promise.allSettled(
        STATIC_ASSETS.map(url =>
          cache.add(url).catch(err => console.warn('[SW] Skip cache:', url, err.message))
        )
      );
    }).then(() => self.skipWaiting())
  );
});

/* ---- ACTIVATE: remove stale cache versions ---- */
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => {
          console.log('[SW] Deleting old cache:', k);
          return caches.delete(k);
        })
      ))
      .then(() => self.clients.claim())
  );
});

/* ---- FETCH: cache-first for static, network-first for API ---- */
self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  if (!req.url.startsWith('http')) return;

  const url = new URL(req.url);
  const isApiCall = NETWORK_FIRST_HOSTS.some(h => url.hostname.includes(h));

  event.respondWith(isApiCall ? networkFirst(req) : cacheFirst(req));
});

// Cache-first: serve from cache, fall back to network + populate cache
async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    if (response.ok && response.status === 200) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    return new Response('Offline — resource not in cache', {
      status: 503, headers: { 'Content-Type': 'text/plain' }
    });
  }
}

// Network-first: try network, fall back to cache for offline support
async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    if (cached) return cached;
    return new Response(JSON.stringify({ offline: true, cached: false }), {
      status: 503, headers: { 'Content-Type': 'application/json' }
    });
  }
}

/* ---- MESSAGES: skipWaiting + cache size query ---- */
self.addEventListener('message', event => {
  if (!event.data) return;

  if (event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  if (event.data.type === 'GET_CACHE_SIZE' && event.ports[0]) {
    getCacheSize().then(bytes => event.ports[0].postMessage({ bytes }));
  }

  if (event.data.type === 'CLEAR_CACHE' && event.ports[0]) {
    caches.delete(CACHE_NAME)
      .then(() => event.ports[0].postMessage({ cleared: true }));
  }
});

async function getCacheSize() {
  try {
    const cache = await caches.open(CACHE_NAME);
    const keys = await cache.keys();
    let total = 0;
    for (const req of keys) {
      const res = await cache.match(req);
      if (res) {
        const buf = await res.clone().arrayBuffer();
        total += buf.byteLength;
      }
    }
    return total;
  } catch { return 0; }
}
