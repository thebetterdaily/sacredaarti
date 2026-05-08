// Sacred Aarti — Service Worker v3
// Network-first for HTML (so updates appear immediately)
// Cache-first for static assets (icons, manifest)

const CACHE_NAME = 'sacred-aarti-v3-2026-05-07';
const BASE = '/sacredaarti';

// Assets that rarely change — safe to cache aggressively
const STATIC_ASSETS = [
  BASE + '/manifest.json',
  BASE + '/icon-192.png',
  BASE + '/icon-512.png',
  BASE + '/apple-touch-icon.png'
];

// Install: pre-cache only static assets (NOT index.html)
self.addEventListener('install', function(e){
  e.waitUntil(
    caches.open(CACHE_NAME).then(function(cache){
      return cache.addAll(STATIC_ASSETS).catch(function(){
        // Don't fail install if some assets are missing
        return Promise.resolve();
      });
    })
  );
  // Activate this new service worker immediately, replacing the old one
  self.skipWaiting();
});

// Activate: delete ALL old caches (any cache name not matching current version)
self.addEventListener('activate', function(e){
  e.waitUntil(
    caches.keys().then(function(keys){
      return Promise.all(
        keys.filter(function(k){ return k !== CACHE_NAME; })
            .map(function(k){ return caches.delete(k); })
      );
    }).then(function(){
      // Take control of all open pages immediately
      return self.clients.claim();
    })
  );
});

// Fetch strategy:
//   - HTML / navigation requests → network-first (always try fresh, fall back to cache offline)
//   - Everything else → cache-first (fast load for icons, manifest, fonts)
self.addEventListener('fetch', function(e){
  var req = e.request;

  // Only handle GET requests
  if(req.method !== 'GET') return;

  var url = new URL(req.url);
  var isHTML = req.mode === 'navigate' ||
               (req.headers.get('accept') || '').indexOf('text/html') !== -1 ||
               url.pathname.endsWith('.html') ||
               url.pathname === BASE + '/' ||
               url.pathname === '/';

  if(isHTML){
    // NETWORK-FIRST for HTML — guarantees users see updates
    e.respondWith(
      fetch(req).then(function(res){
        // Cache the fresh response for offline use
        if(res && res.status === 200){
          var clone = res.clone();
          caches.open(CACHE_NAME).then(function(c){ c.put(req, clone); });
        }
        return res;
      }).catch(function(){
        // Offline — fall back to cached version
        return caches.match(req).then(function(cached){
          return cached || caches.match(BASE + '/index.html') || caches.match(BASE + '/');
        });
      })
    );
  } else {
    // CACHE-FIRST for static assets — fast loading
    e.respondWith(
      caches.match(req).then(function(cached){
        if(cached) return cached;
        return fetch(req).then(function(res){
          if(res && res.status === 200 && res.type === 'basic'){
            var clone = res.clone();
            caches.open(CACHE_NAME).then(function(c){ c.put(req, clone); });
          }
          return res;
        });
      })
    );
  }
});
