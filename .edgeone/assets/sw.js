// LaserWeld Pro Service Worker v1.0
// 离线时显示已缓存的内容
const CACHE_NAME = 'laserweld-pro-v1';
const ASSETS_TO_CACHE = [
  './index.html',
  './manifest.json',
  './data/params.js',
  './data/articles.js',
  './data/sub-factors.js',
  './favicon.svg',
  './banners/banner-1.jpg',
  './banners/banner-2.jpg',
  './banners/banner-3.jpg'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      );
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached || fetch(event.request).catch(() => cached);
    })
  );
});
