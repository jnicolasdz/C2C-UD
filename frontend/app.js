const page = document.body.dataset.page;
const useProxy = window.location.protocol.startsWith('http') && window.location.port === '8080';

const API = {
  coupon: useProxy ? '/api/coupon' : 'http://localhost:8001/api/v1',
  email: useProxy ? '/api/email' : 'http://localhost:8002/api/v1',
  geolocation: useProxy ? '/api/geolocation' : 'http://localhost:8003/api/v1',
  report: useProxy ? '/api/report/reports' : 'http://localhost:8004/api/v1/reports',
  reportRoot: useProxy ? '/api/report' : 'http://localhost:8004/api/v1'
};

const state = {
  user: JSON.parse(localStorage.getItem('c2cUser') || 'null') || {
    user_name: 'Juan Sebastián Henríquez',
    user_email: 'jsebastian.henriquezb@udistrital.edu.co',
    user_id: '20221020058'
  },
  locations: [],
  reports: [],
  coupons: [],
  maps: {},
  markerLayers: {}
};

const endpoints = [
  ['coupon','GET','/coupons','Listar todos los cupones'],
  ['coupon','GET','/coupons/code/{code}','Consultar cupón por código'],
  ['coupon','GET','/coupons/creation-date/{date}','Filtrar por fecha de creación'],
  ['coupon','GET','/coupons/expiration-date/{date}','Filtrar por fecha de expiración'],
  ['coupon','GET','/coupons/expired','Cupones expirados'],
  ['coupon','GET','/coupons/valid','Cupones válidos'],
  ['coupon','GET','/coupons/enabled','Cupones habilitados'],
  ['coupon','GET','/coupons/disabled','Cupones deshabilitados'],
  ['coupon','GET','/coupons/search/{text}','Buscar por texto'],
  ['coupon','GET','/coupons/happy-birthday','Cupones de cumpleaños'],
  ['coupon','GET','/coupons/referred','Cupones de referido'],
  ['coupon','GET','/coupons/last/{text}','Último cupón por texto'],
  ['coupon','POST','/coupons/unassigned?text=&discount=&days=','Crear cupón público'],
  ['coupon','POST','/coupons/assigned?text=&discount=&days=&user_email=','Crear cupón asignado'],
  ['coupon','POST','/coupons/happy-birthday/{user_email}','Crear cupón cumpleaños'],
  ['coupon','POST','/coupons/referred/{user_email}','Crear cupón referido'],
  ['coupon','POST','/coupons/{code}/enable','Habilitar cupón'],
  ['coupon','POST','/coupons/{code}/disable','Deshabilitar cupón'],
  ['coupon','GET','/coupons/{code}/is-enabled','Validar habilitado'],
  ['coupon','DELETE','/coupons/{code}','Eliminar cupón'],
  ['coupon','GET','/users/{email}/coupons','Consultar cupones del usuario'],
  ['coupon','GET','/users/coupons/all','Todos los usuarios con cupones'],
  ['coupon','DELETE','/users/{email}/coupons/{coupon_code}','Eliminar cupón asignado del usuario'],
  ['coupon','POST','/users/{email}/coupons/{coupon_code}/apply-assigned?original_price=','Aplicar cupón asignado'],
  ['coupon','POST','/users/{email}/coupons/{coupon_code}/apply-unassigned?original_price=','Aplicar cupón público'],
  ['geolocation','GET','/geolocation/all_address','Listar sedes'],
  ['geolocation','GET','/geolocation/id/{location_id}','Buscar sede por ID'],
  ['geolocation','GET','/geolocation/name/{name}','Buscar sede por nombre'],
  ['geolocation','GET','/geolocation/address/{address}','Buscar sede por dirección'],
  ['geolocation','POST','/geolocation/add/{name}/{description}/{address}/{latitude}/{longitude}','Crear punto geográfico'],
  ['geolocation','DELETE','/geolocation/{location_id}','Eliminar punto geográfico'],
  ['report','POST','/reports/','Crear reporte'],
  ['report','GET','/reports/','Listar reportes con filtros'],
  ['report','GET','/reports/failed','Listar reportes fallidos'],
  ['report','GET','/reports/pending','Listar reportes pendientes'],
  ['report','GET','/reports/tracking/{radicado}','Seguimiento por radicado'],
  ['report','GET','/reports/{report_id}','Consultar reporte por ID'],
  ['report','PUT','/reports/{report_id}','Actualizar reporte'],
  ['report','POST','/reports/{report_id}/retry','Reintentar notificación'],
  ['report','DELETE','/reports/{report_id}','Eliminar reporte lógico'],
  ['email','GET','/health','Health del servicio email'],
  ['email','GET','/emails/health','Health alterno del servicio email'],
  ['email','GET','/email','Información base del servicio email'],
  ['email','POST','/emails/auth/register-confirmation','Correo confirmación registro'],
  ['email','POST','/emails/auth/email-verification','Correo verificación'],
  ['email','POST','/emails/auth/send-otp','Correo OTP'],
  ['email','POST','/emails/auth/password-changed','Correo cambio contraseña'],
  ['email','POST','/emails/promotions/discount-available','Correo descuento disponible'],
  ['email','POST','/emails/promotions/birthday','Correo cumpleaños'],
  ['email','POST','/emails/promotions/general','Correo promoción general'],
  ['email','POST','/emails/promotions/welcome','Correo bienvenida'],
  ['email','POST','/emails/moderation/account-suspended','Correo cuenta suspendida'],
  ['email','POST','/emails/moderation/product-rejected','Correo producto rechazado'],
  ['email','POST','/emails/moderation/policies-updated','Correo políticas'],
  ['email','POST','/emails/newsletters/news','Correo newsletter'],
  ['email','POST','/emails/newsletters/new-sellers','Correo nuevos vendedores'],
  ['email','POST','/emails/referrals/invitation','Correo invitación referido'],
  ['email','POST','/emails/referrals/reward','Correo recompensa referido']
];

function $(selector, root = document) { return root.querySelector(selector); }
function $all(selector, root = document) { return [...root.querySelectorAll(selector)]; }
function asJson(value) { return JSON.stringify(value, null, 2); }
function encode(value) { return encodeURIComponent(value); }
function money(value) { return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(Number(value || 0)); }
function todayIso() { return new Date().toISOString(); }
function dateOnly(days = 0) { const d = new Date(); d.setDate(d.getDate() + days); return d.toISOString().slice(0,10); }

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function formData(form) {
  const data = Object.fromEntries(new FormData(form).entries());
  $all('input[type="checkbox"]', form).forEach(input => data[input.name] = input.checked);
  return data;
}

async function apiFetch(url, options = {}) {
  const headers = options.headers || {};
  const config = { ...options, headers };
  if (config.body && typeof config.body !== 'string') {
    config.body = JSON.stringify(config.body);
    config.headers = { 'Content-Type': 'application/json', ...headers };
  }
  const response = await fetch(url, config);
  const raw = await response.text();
  let data = raw;
  try { data = raw ? JSON.parse(raw) : null; } catch (_) {}
  if (!response.ok) {
    const message = typeof data === 'object' ? (data.detail?.message || data.detail || data.message || response.statusText) : data;
    throw new Error(`${response.status} ${response.statusText}: ${typeof message === 'string' ? message : JSON.stringify(message)}`);
  }
  return data;
}

function setOutput(id, value) {
  const el = $(id.startsWith('#') ? id : `#${id}`);
  if (el) el.textContent = typeof value === 'string' ? value : asJson(value);
}

function setStatus(service, status, text) {
  $all(`#status-${service}`).forEach(el => {
    el.className = `pill ${status}`;
    el.textContent = text;
  });
}

async function checkService(service) {
  try {
    if (service === 'coupon') await apiFetch(`${API.coupon}/coupons`);
    if (service === 'email') await apiFetch(`${API.email}/health`);
    if (service === 'geolocation') await apiFetch(`${API.geolocation}/geolocation/all_address`);
    if (service === 'report') await apiFetch(`${API.report}/`);
    setStatus(service, 'ok', `${labelService(service)} activo`);
    return true;
  } catch (error) {
    setStatus(service, 'bad', `${labelService(service)} sin conexión`);
    return false;
  }
}

function labelService(service) {
  return { coupon:'Cupones', email:'Correos', geolocation:'Geolocalización', report:'Reportes' }[service] || service;
}

async function checkAllServices() {
  await Promise.all(['coupon','email','geolocation','report'].map(checkService));
}

function initShared() {
  $all('#btn-check-all').forEach(btn => btn.addEventListener('click', checkAllServices));
  checkAllServices();
}

function saveUserSession(data) {
  state.user = { ...state.user, ...data };
  localStorage.setItem('c2cUser', JSON.stringify(state.user));
}

function fillUserSessionForm() {
  const form = $('#user-session-form');
  if (!form) return;
  Object.entries(state.user).forEach(([key, value]) => {
    const field = form.elements[key];
    if (field) field.value = value;
  });
}

function reportPayload(extra = {}) {
  return {
    user_id: state.user.user_id,
    user_name: state.user.user_name,
    user_email: state.user.user_email,
    report_type: extra.report_type || 'PUBLICACION_INAPROPIADA',
    subject: extra.subject || 'Producto con información sospechosa',
    description: extra.description || 'El vendedor publicó un producto con datos incompletos y solicita pago por fuera de la plataforma.'
  };
}

async function createReport(payload, outputId) {
  const response = await apiFetch(`${API.report}/`, { method: 'POST', body: payload });
  if (response?.report?.radicado) {
    const trackingInput = $('#tracking-form input[name="radicado"]');
    if (trackingInput) trackingInput.value = response.report.radicado;
    renderReportFlow(response.report.status);
  }
  setOutput(outputId, response);
  return response;
}

function renderReportFlow(status = 'RECIBIDO') {
  const el = $('#report-status-diagram');
  if (!el) return;
  const steps = ['RECIBIDO','EN_REVISION','EN_PROCESO','RESUELTO'];
  const activeIndex = Math.max(0, steps.indexOf(status));
  el.innerHTML = steps.map((step, index) => `${index ? '<i></i>' : ''}<span class="${index <= activeIndex ? 'active' : ''}">${step}</span>`).join('');
}

async function loadLocations(target = 'user') {
  const response = await apiFetch(`${API.geolocation}/geolocation/all_address`);
  state.locations = normalizeLocations(response);
  renderMap(`${target}-map`, state.locations, loc => selectLocation(loc, target));
  renderLocationTable(target);
  renderRouteDiagram(`${target}-route-diagram`, state.locations);
  return state.locations;
}

function normalizeLocations(response) {
  if (response?.error) throw new Error(response.error);
  if (Array.isArray(response)) return response.filter(isValidLocation);
  if (response && isValidLocation(response)) return [response];
  return [];
}

function normalizeLocation(response) {
  if (response?.error) throw new Error(response.error);
  if (!isValidLocation(response)) throw new Error('La respuesta no contiene una sede con latitude y longitude válidas.');
  return response;
}

function isValidLocation(loc) {
  return loc && loc.id !== undefined && loc.name && loc.latitude !== undefined && loc.longitude !== undefined && !Number.isNaN(Number(loc.latitude)) && !Number.isNaN(Number(loc.longitude));
}

function bogotaCenter() { return [4.615281339898904, -74.09331682907303]; }
function locationLatLng(loc) { return [Number(loc.latitude), Number(loc.longitude)]; }

function renderMap(id, locations, onSelect, selectedId = null) {
  if (window.L) return renderLeafletMap(id, locations, onSelect, selectedId);
  return renderStaticMap(id, locations, onSelect);
}

function renderLeafletMap(id, locations, onSelect, selectedId = null) {
  const el = $(`#${id}`);
  if (!el) return;

  el.classList.add('leaflet-ready');
  if (el.clientHeight < 320) el.style.height = '520px';

  if (!state.maps[id]) {
    state.maps[id] = L.map(el, {
      center: bogotaCenter(),
      zoom: 12,
      scrollWheelZoom: true,
      zoomControl: true,
      preferCanvas: true
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap',
      maxZoom: 19,
      crossOrigin: true
    }).addTo(state.maps[id]);

    state.markerLayers[id] = L.layerGroup().addTo(state.maps[id]);
  }

  const map = state.maps[id];
  const layer = state.markerLayers[id];
  layer.clearLayers();

  const validLocations = locations.filter(isValidLocation);
  const bounds = [];

  validLocations.forEach(loc => {
    const latLng = locationLatLng(loc);
    bounds.push(latLng);
    const selected = String(loc.id) === String(selectedId);
    const marker = L.marker(latLng, {
      title: `${loc.id} · ${loc.name}`,
      icon: L.divIcon({
        className: `ud-leaflet-pin${selected ? ' selected' : ''}`,
        html: `<span><b>${escapeHtml(loc.id)}</b></span>`,
        iconSize: [34, 44],
        iconAnchor: [17, 40],
        popupAnchor: [0, -38]
      })
    }).addTo(layer);

    marker.bindTooltip(`${loc.id} · ${escapeHtml(loc.name)}`, {
      permanent: selected,
      direction: 'top',
      offset: [0, -34],
      className: 'ud-map-tooltip'
    });

    marker.bindPopup(`
      <strong>${escapeHtml(loc.name)}</strong><br>
      <span>${escapeHtml(loc.address || 'Sin dirección registrada')}</span><br>
      <small>ID ${escapeHtml(loc.id)} · ${escapeHtml(loc.latitude)}, ${escapeHtml(loc.longitude)}</small>
    `);

    marker.on('click', () => onSelect?.(loc));
  });

  const resizeMap = () => map.invalidateSize({ pan: false, debounceMoveend: true });
  requestAnimationFrame(resizeMap);
  setTimeout(resizeMap, 120);
  setTimeout(resizeMap, 450);

  if (selectedId && validLocations.some(loc => String(loc.id) === String(selectedId))) {
    const selectedLoc = validLocations.find(loc => String(loc.id) === String(selectedId));
    setTimeout(() => map.setView(locationLatLng(selectedLoc), 16, { animate: true }), 140);
  } else if (bounds.length > 1) {
    setTimeout(() => map.fitBounds(bounds, { padding: [48, 48], maxZoom: 14 }), 140);
  } else if (bounds.length === 1) {
    setTimeout(() => map.setView(bounds[0], 16), 140);
  } else {
    map.setView(bogotaCenter(), 12);
  }
}

function renderStaticMap(id, locations, onSelect) {
  const map = $(`#${id}`);
  if (!map) return;
  map.innerHTML = '<div class="map-watermark">Bogotá · modo sin Leaflet</div>';
  const bounds = { minLat: 4.50, maxLat: 4.75, minLng: -74.22, maxLng: -73.98 };
  locations.filter(isValidLocation).forEach(loc => {
    const x = ((Number(loc.longitude) - bounds.minLng) / (bounds.maxLng - bounds.minLng)) * 100;
    const y = (1 - ((Number(loc.latitude) - bounds.minLat) / (bounds.maxLat - bounds.minLat))) * 100;
    const marker = document.createElement('button');
    marker.className = 'marker';
    marker.type = 'button';
    marker.style.left = `${Math.min(95, Math.max(5, x))}%`;
    marker.style.top = `${Math.min(92, Math.max(8, y))}%`;
    marker.dataset.label = loc.name;
    marker.title = `${loc.name} · ${loc.address}`;
    marker.textContent = loc.id;
    marker.addEventListener('click', () => onSelect?.(loc));
    map.appendChild(marker);
  });
}

function selectLocation(loc, target = 'user') {
  const location = normalizeLocation(loc);
  const box = target === 'admin' ? $('#geo-admin-output') : $('#geo-selected');
  if (box) {
    box.textContent = `Sede seleccionada:
${location.name}
ID: ${location.id}
Dirección: ${location.address}
Coordenadas: ${location.latitude}, ${location.longitude}
Descripción: ${location.description}`;
  }
  const base = state.locations.length ? state.locations : [location];
  const merged = base.some(item => String(item.id) === String(location.id)) ? base : [...base, location];
  renderMap(`${target}-map`, merged, selected => selectLocation(selected, target), location.id);
  renderRouteDiagram(`${target}-route-diagram`, merged, location);
}

async function searchLocation(mode, query, target = 'user') {
  const paths = {
    id: `/geolocation/id/${encode(query)}`,
    name: `/geolocation/name/${encode(query)}`,
    address: `/geolocation/address/${encode(query)}`
  };
  const path = paths[mode] || paths.id;
  const response = await apiFetch(`${API.geolocation}${path}`);
  const loc = normalizeLocation(response);
  selectLocation(loc, target);
  return loc;
}

function renderRouteDiagram(id, locations, selected = null) {
  const el = $(`#${id}`);
  if (!el) return;
  if (!locations.length && !selected) {
    el.innerHTML = '<div class="empty-state">No hay sedes para construir el diagrama.</div>';
    return;
  }
  const selectedLoc = selected || locations[0];
  el.innerHTML = `
    <div class="route-node"><strong>Frontend</strong><span>Usuario/admin solicita una sede o lista completa.</span></div>
    <div class="route-node"><strong>Servicio geolocation</strong><span>Consulta endpoint exacto y retorna id, name, address, latitude, longitude.</span></div>
    <div class="route-node"><strong>${selectedLoc.name}</strong><span>${selectedLoc.address}<br>${selectedLoc.latitude}, ${selectedLoc.longitude}</span></div>
    <div class="route-node"><strong>Leaflet + OpenStreetMap</strong><span>Se centra el mapa en Bogotá y se dibuja el marcador real.</span></div>
  `;
}

function renderLocationTable(target = 'admin') {
  const container = target === 'admin' ? $('#admin-location-list') : null;
  if (!container) return;
  if (!state.locations.length) {
    container.className = 'table-wrap mt-md empty-state';
    container.textContent = 'No hay sedes cargadas.';
    return;
  }
  container.className = 'table-wrap mt-md';
  container.innerHTML = `
    <table class="data-table">
      <thead><tr><th>ID</th><th>Nombre</th><th>Dirección</th><th>Coordenadas</th><th>Acción</th></tr></thead>
      <tbody>${state.locations.map(loc => `
        <tr>
          <td>${loc.id}</td>
          <td><strong>${loc.name}</strong><br><small>${loc.description}</small></td>
          <td>${loc.address}</td>
          <td>${loc.latitude}<br>${loc.longitude}</td>
          <td><button class="tiny primary" data-select-location="${loc.id}">Centrar</button></td>
        </tr>`).join('')}</tbody>
    </table>`;
  $all('[data-select-location]', container).forEach(btn => btn.addEventListener('click', () => {
    const loc = state.locations.find(item => String(item.id) === btn.dataset.selectLocation);
    if (loc) selectLocation(loc, 'admin');
  }));
}

async function loadUserCoupons() {
  try {
    const data = await apiFetch(`${API.coupon}/users/${encode(state.user.user_email)}/coupons`);
    renderUserCoupons(data);
    return data;
  } catch (error) {
    const el = $('#user-coupon-list');
    if (el) {
      el.className = 'coupon-grid empty-state';
      el.textContent = `No hay cupones para este usuario o aún no existen: ${error.message}`;
    }
  }
}

function renderUserCoupons(data) {
  const el = $('#user-coupon-list');
  if (!el) return;
  const assigned = data.assigned_coupons || [];
  const unassigned = data.unassigned_coupons || [];
  const all = [...assigned.map(c => ({...c, mode:'Asignado'})), ...unassigned.map(c => ({...c, mode:'Usado público'}))];
  if (!all.length) {
    el.className = 'coupon-grid empty-state';
    el.textContent = 'El usuario no tiene cupones asignados ni consumidos.';
    return;
  }
  el.className = 'coupon-grid';
  el.innerHTML = all.map(coupon => `
    <article class="coupon-card">
      <strong>${coupon.code}</strong>
      <span>${coupon.text} · ${coupon.mode}</span>
      <span>Descuento: ${(Number(coupon.discount) * 100).toFixed(0)}%</span>
      <span>Vence: ${String(coupon.expiration_date).slice(0,10)}</span>
      <button class="tiny primary" data-copy-coupon="${coupon.code}">Usar código</button>
    </article>`).join('');
  $all('[data-copy-coupon]', el).forEach(btn => btn.addEventListener('click', () => {
    const input = $('#apply-coupon-form input[name="coupon_code"]');
    if (input) input.value = btn.dataset.copyCoupon;
  }));
}

async function loadCoupons() {
  const data = await apiFetch(`${API.coupon}/coupons`);
  state.coupons = Array.isArray(data) ? data : [];
  renderCouponTable(state.coupons);
  return state.coupons;
}

function renderCouponTable(coupons) {
  const container = $('#coupon-table');
  if (!container) return;
  if (!coupons.length) {
    container.className = 'table-wrap mt-md empty-state';
    container.textContent = 'No hay cupones cargados.';
    return;
  }
  container.className = 'table-wrap mt-md';
  container.innerHTML = `
    <table class="data-table">
      <thead><tr><th>Código</th><th>Texto</th><th>Descuento</th><th>Vigencia</th><th>Estado</th><th>Acciones</th></tr></thead>
      <tbody>${coupons.map(c => `
        <tr>
          <td><strong>${c.code}</strong></td>
          <td>${c.text}</td>
          <td>${(Number(c.discount) * 100).toFixed(0)}%</td>
          <td>${String(c.creation_date).slice(0,10)} → ${String(c.expiration_date).slice(0,10)}</td>
          <td><span class="pill ${c.enabled ? 'ok' : 'bad'}">${c.enabled ? 'Habilitado' : 'Deshabilitado'}</span></td>
          <td><div class="table-actions">
            <button class="tiny primary" data-coupon-action="copy" data-code="${c.code}">Copiar</button>
            <button class="tiny" data-coupon-action="toggle" data-code="${c.code}" data-enabled="${c.enabled}">${c.enabled ? 'Deshabilitar' : 'Habilitar'}</button>
            <button class="tiny danger" data-coupon-action="delete" data-code="${c.code}">Eliminar</button>
          </div></td>
        </tr>`).join('')}</tbody>
    </table>`;
  $all('[data-coupon-action]', container).forEach(btn => btn.addEventListener('click', async () => {
    const code = btn.dataset.code;
    if (btn.dataset.couponAction === 'copy') {
      const input = $('#coupon-code-action-form input[name="coupon_code"]');
      if (input) input.value = code;
      return;
    }
    const action = btn.dataset.couponAction === 'delete' ? 'delete' : (btn.dataset.enabled === 'true' ? 'disable' : 'enable');
    await runCouponCodeAction(code, action);
  }));
}

async function runCouponCodeAction(code, action) {
  let response;
  if (action === 'enable') response = await apiFetch(`${API.coupon}/coupons/${encode(code)}/enable`, { method:'POST' });
  if (action === 'disable') response = await apiFetch(`${API.coupon}/coupons/${encode(code)}/disable`, { method:'POST' });
  if (action === 'delete') response = await apiFetch(`${API.coupon}/coupons/${encode(code)}`, { method:'DELETE' });
  if (action === 'is-enabled') response = await apiFetch(`${API.coupon}/coupons/${encode(code)}/is-enabled`);
  setOutput('coupon-admin-output', response);
  await loadCoupons();
}

async function createCouponFromForm(data) {
  const email = data.user_email || state.user.user_email;
  let url = '';
  if (data.creation_type === 'assigned') {
    url = `${API.coupon}/coupons/assigned?text=${encode(data.text)}&discount=${encode(data.discount)}&days=${encode(data.days)}&user_email=${encode(email)}`;
  } else if (data.creation_type === 'birthday') {
    url = `${API.coupon}/coupons/happy-birthday/${encode(email)}`;
  } else if (data.creation_type === 'referred') {
    url = `${API.coupon}/coupons/referred/${encode(email)}`;
  } else {
    url = `${API.coupon}/coupons/unassigned?text=${encode(data.text)}&discount=${encode(data.discount)}&days=${encode(data.days)}`;
  }
  const response = await apiFetch(url, { method:'POST' });
  setOutput('coupon-admin-output', response);
  await loadCoupons();
}

async function seedCoupons() {
  const email = state.user.user_email;
  const stamp = String(Date.now()).slice(-4);
  const cases = [
    `${API.coupon}/coupons/unassigned?text=WELCOMEUD${stamp}&discount=0.15&days=30`,
    `${API.coupon}/coupons/assigned?text=TOPUD${stamp}&discount=0.20&days=15&user_email=${encode(email)}`,
    `${API.coupon}/coupons/happy-birthday/${encode(email)}`,
    `${API.coupon}/coupons/referred/${encode(email)}`
  ];
  const results = [];
  for (const url of cases) {
    try { results.push(await apiFetch(url, { method:'POST' })); }
    catch (error) { results.push({ error: error.message, url }); }
  }
  setOutput('coupon-admin-output', results);
  await loadCoupons();
}

async function loadReports(params = {}) {
  const qs = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '' && value !== false) qs.set(key, value);
    if (key === 'include_deleted' && value === true) qs.set(key, 'true');
  });
  const url = `${API.report}/?${qs.toString()}`;
  const data = await apiFetch(url);
  state.reports = Array.isArray(data) ? data : [];
  renderReportsTable(state.reports);
  renderReportsStats(state.reports);
  return state.reports;
}

function renderReportsStats(reports) {
  const total = reports.length;
  const sent = reports.filter(r => r.send_status === 'ENVIADO').length;
  const pending = reports.filter(r => r.send_status === 'PENDIENTE').length;
  const failed = reports.filter(r => r.send_status === 'FALLIDO').length;
  const map = { 'stat-total-reports': total, 'stat-sent-reports': sent, 'stat-pending-reports': pending, 'stat-failed-reports': failed };
  Object.entries(map).forEach(([id, value]) => { const el = $(`#${id}`); if (el) el.textContent = value; });
  renderBarChart('reports-chart', [ ['ENVIADO', sent], ['PENDIENTE', pending], ['FALLIDO', failed] ]);
}

function renderBarChart(id, rows) {
  const el = $(`#${id}`);
  if (!el) return;
  const max = Math.max(1, ...rows.map(r => r[1]));
  el.className = 'bar-chart';
  el.innerHTML = rows.map(([label, value]) => `
    <div class="bar-row"><strong>${label}</strong><div class="bar-track"><div class="bar-fill" style="width:${(value/max)*100}%"></div></div><span>${value}</span></div>
  `).join('');
}

function renderReportsTable(reports) {
  const container = $('#reports-table');
  if (!container) return;
  if (!reports.length) {
    container.className = 'table-wrap mt-md empty-state';
    container.textContent = 'No hay reportes cargados.';
    return;
  }
  container.className = 'table-wrap mt-md';
  container.innerHTML = `
    <table class="data-table">
      <thead><tr><th>ID</th><th>Radicado</th><th>Usuario</th><th>Tipo</th><th>Estado</th><th>Envío</th><th>Acciones</th></tr></thead>
      <tbody>${reports.map(r => `
        <tr>
          <td>${r.id}</td>
          <td><strong>${r.radicado}</strong><br><small>${String(r.created_at).slice(0,16).replace('T',' ')}</small></td>
          <td>${r.user_name}<br><small>${r.user_email}</small></td>
          <td>${r.report_type}<br><small>${r.subject}</small></td>
          <td><span class="pill warn">${r.status}</span></td>
          <td><span class="pill ${r.send_status === 'ENVIADO' ? 'ok' : r.send_status === 'FALLIDO' ? 'bad' : 'warn'}">${r.send_status}</span></td>
          <td><div class="table-actions">
            <button class="tiny primary" data-report-action="edit" data-id="${r.id}">Editar</button>
            <button class="tiny" data-report-action="retry" data-id="${r.id}">Reintentar</button>
            <button class="tiny danger" data-report-action="delete" data-id="${r.id}">Eliminar</button>
          </div></td>
        </tr>`).join('')}</tbody>
    </table>`;
  $all('[data-report-action]', container).forEach(btn => btn.addEventListener('click', async () => {
    const id = btn.dataset.id;
    if (btn.dataset.reportAction === 'edit') {
      const form = $('#update-report-form');
      if (form) form.elements.report_id.value = id;
      document.getElementById('update-report-form')?.scrollIntoView({behavior:'smooth', block:'center'});
    }
    if (btn.dataset.reportAction === 'retry') {
      const response = await apiFetch(`${API.report}/${id}/retry`, { method:'POST' });
      setOutput('report-admin-output', response);
      await loadReports();
    }
    if (btn.dataset.reportAction === 'delete') {
      const response = await apiFetch(`${API.report}/${id}`, { method:'DELETE' });
      setOutput('report-admin-output', response);
      await loadReports();
    }
  }));
}

function buildEmailPayload(template, correo, nombre) {
  const recipient = { codigo_user: 20221020058, correo_institu: correo, primer_nomb: nombre };
  const common = { codigo_user: 20221020058, correo_institu: correo, primer_nomb: nombre };
  const map = {
    'register-confirmation': { endpoint:'/emails/auth/register-confirmation', body:{ ...common, segundo_nom:'', primer_apel:'Henríquez' } },
    'email-verification': { endpoint:'/emails/auth/email-verification', body:{ ...common, verification_code:'UD2026', expiration_minutes:15 } },
    'send-otp': { endpoint:'/emails/auth/send-otp', body:{ ...common, otp_code:'123456', expiration_minutes:5, device_hint:'Navegador de prueba' } },
    'password-changed': { endpoint:'/emails/auth/password-changed', body:{ ...common, fecha_cambio: todayIso().replace(/\.\d{3}Z$/, 'Z'), ip_origen:'127.0.0.1' } },
    'discount-available': { endpoint:'/emails/promotions/discount-available', body:{ ...common, id_cupon:1, id_pub:10, nombre_pub:'Libro de Cálculo usado', precio_original:85000, precio_con_descuento:72250, porcentaje_descuento:15, descripcion_prom:'Descuento de bienvenida UD', fecha_inicio:dateOnly(), fecha_fin:dateOnly(30) } },
    'birthday': { endpoint:'/emails/promotions/birthday', body:{ ...common, id_cupon:2, fecha_fin_cupon:dateOnly(30), descripcion_prom:'Cupón especial de cumpleaños' } },
    'general': { endpoint:'/emails/promotions/general', body:{ recipients:[recipient], id_prom:7, tipo_prom:'Feria universitaria', descripcion_prom:'Promoción para productos académicos de la comunidad UD', fecha_fin_prom:dateOnly(15) } },
    'welcome': { endpoint:'/emails/promotions/welcome', body:{ ...common, id_cupon:3, fecha_fin_cupon:dateOnly(20), descripcion_prom:'Bienvenida al marketplace C2C-UD' } },
    'account-suspended': { endpoint:'/emails/moderation/account-suspended', body:{ ...common, motivo_suspension:'Actividad inusual detectada en publicación', numero_contrato:1001, fecha_suspension:todayIso().replace(/\.\d{3}Z$/, 'Z'), instrucciones_apelacion:'Responder este correo con la evidencia de soporte.' } },
    'product-rejected': { endpoint:'/emails/moderation/product-rejected', body:{ ...common, id_pub:99, nombre_pub:'Producto sin evidencia', motivo_rechazo:'No cumple las políticas de publicación', numero_contrato:1002, recomendaciones:'Actualizar fotos, descripción y precio.' } },
    'policies-updated': { endpoint:'/emails/moderation/policies-updated', body:{ recipients:[recipient], id_doc:4, tipo_doc:'Términos y condiciones', version_nueva:'1.1', resumen_cambios:'Se actualizan reglas de publicación y seguridad.', numero_contrato:1003, enlace_documento:'https://udistrital.edu.co', fecha_vigencia:dateOnly(7) } },
    'news': { endpoint:'/emails/newsletters/news', body:{ recipients:[recipient], titulo_boletin:'Novedades C2C-UD', contenido_html:'<p>Conoce nuevas publicaciones, sedes y beneficios para estudiantes.</p>', fecha_publicacion:dateOnly() } },
    'new-sellers': { endpoint:'/emails/newsletters/new-sellers', body:{ recipients:[recipient], new_sellers:[{ codigo_user:55, nombre_vendedor:'Tienda Académica UD', calificacion:4.8, id_categoria:3, nombre_categoria:'Libros' }], titulo_boletin:'Nuevos vendedores destacados', fecha_publicacion:dateOnly() } },
    'referral-invitation': { endpoint:'/emails/referrals/invitation', body:{ referrer_codigo_user:20221020058, referrer_nombre:nombre, invitee_correo:correo, referral_code:'UD-REF-2026', referral_link:'https://marketplace.udistrital.edu.co/ref/UD-REF-2026', mensaje_personalizado:'Únete al marketplace de la comunidad UD.' } },
    'referral-reward': { endpoint:'/emails/referrals/reward', body:{ ...common, referred_user_nombre:'Compañero UD', recompensa_descripcion:'Cupón de referido del 15%', id_cupon_recompensa:8 } }
  };
  return map[template];
}

function renderEndpointMatrix() {
  const container = $('#endpoint-matrix');
  if (!container) return;
  container.className = 'table-wrap';
  container.innerHTML = `
    <table class="data-table">
      <thead><tr><th>Servicio</th><th>Método</th><th>Endpoint</th><th>Uso</th></tr></thead>
      <tbody>${endpoints.map(([service, method, endpoint, use]) => `
        <tr><td><strong>${labelService(service)}</strong></td><td>${method}</td><td><code>${endpoint}</code></td><td>${use}</td></tr>`).join('')}</tbody>
    </table>`;
}

function initHome() {
  $('#btn-check-all')?.addEventListener('click', checkAllServices);
}

function initUser() {
  fillUserSessionForm();
  $('#user-session-form')?.addEventListener('submit', event => {
    event.preventDefault();
    saveUserSession(formData(event.currentTarget));
    event.currentTarget.querySelector('button').textContent = 'Datos guardados';
    setTimeout(() => event.currentTarget.querySelector('button').textContent = 'Guardar datos', 1300);
  });
  $('#fill-report-case')?.addEventListener('click', () => {
    const form = $('#user-report-form');
    form.elements.report_type.value = 'FRAUDE';
    form.elements.subject.value = 'Solicitud de pago por fuera de la plataforma';
    form.elements.description.value = 'El vendedor pide transferencia externa antes de entregar el producto. Se adjuntaría evidencia en una versión futura del módulo.';
  });
  $('#user-report-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try { await createReport(reportPayload(formData(event.currentTarget)), 'user-report-result'); }
    catch (error) { setOutput('user-report-result', error.message); }
  });
  $('#tracking-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const data = formData(event.currentTarget);
      const response = await apiFetch(`${API.report}/tracking/${encode(data.radicado)}`);
      setOutput('tracking-output', response);
      renderReportFlow(response.status);
    } catch (error) { setOutput('tracking-output', error.message); }
  });
  $('#btn-load-user-locations')?.addEventListener('click', () => loadLocations('user').catch(err => setOutput('geo-selected', err.message)));
  $('#geo-search-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const data = formData(event.currentTarget);
      await searchLocation(data.mode, data.query, 'user');
    } catch (error) { setOutput('geo-selected', error.message); }
  });
  $('#btn-load-user-coupons')?.addEventListener('click', loadUserCoupons);
  $('#apply-coupon-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const data = formData(event.currentTarget);
      const suffix = data.mode === 'assigned' ? 'apply-assigned' : 'apply-unassigned';
      const response = await apiFetch(`${API.coupon}/users/${encode(state.user.user_email)}/coupons/${encode(data.coupon_code)}/${suffix}?original_price=${encode(data.original_price)}`, { method:'POST' });
      const display = { ...response, precio_original: money(data.original_price), precio_final: money(response.final_price), ahorro: money(Number(data.original_price) - Number(response.final_price)) };
      setOutput('coupon-user-output', display);
      await loadUserCoupons();
    } catch (error) { setOutput('coupon-user-output', error.message); }
  });
  loadLocations('user').catch(() => {});
}

function initAdmin() {
  $('#btn-load-reports')?.addEventListener('click', () => loadReports().catch(err => setOutput('report-admin-output', err.message)));
  $('#btn-load-pending-reports')?.addEventListener('click', async () => {
    try {
      const data = await apiFetch(`${API.report}/pending`);
      state.reports = Array.isArray(data) ? data : [];
      renderReportsTable(state.reports);
      renderReportsStats(state.reports);
      setOutput('report-admin-output', data);
    } catch (error) { setOutput('report-admin-output', error.message); }
  });
  $('#btn-load-failed-reports')?.addEventListener('click', async () => {
    try {
      const data = await apiFetch(`${API.report}/failed`);
      state.reports = Array.isArray(data) ? data : [];
      renderReportsTable(state.reports);
      renderReportsStats(state.reports);
      setOutput('report-admin-output', data);
    } catch (error) { setOutput('report-admin-output', error.message); }
  });
  $('#report-id-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const d = formData(event.currentTarget);
      const response = await apiFetch(`${API.report}/${encode(d.report_id)}`);
      setOutput('report-admin-output', response);
    } catch (error) { setOutput('report-admin-output', error.message); }
  });
  $('#btn-seed-report')?.addEventListener('click', async () => {
    try {
      const response = await createReport(reportPayload({ report_type:'PRODUCTO_PROHIBIDO', subject:'Caso demo admin: publicación por revisar', description:'Reporte creado desde el panel admin para mostrar el flujo de revisión y actualización de estado.' }), 'report-admin-output');
      await loadReports();
      return response;
    } catch (error) { setOutput('report-admin-output', error.message); }
  });
  $('#report-filter-form')?.addEventListener('submit', event => {
    event.preventDefault();
    loadReports(formData(event.currentTarget)).catch(err => setOutput('report-admin-output', err.message));
  });
  $('#update-report-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const data = formData(event.currentTarget);
      const body = { status: data.status, delivery_message: data.delivery_message };
      const response = await apiFetch(`${API.report}/${data.report_id}`, { method:'PUT', body });
      setOutput('report-admin-output', response);
      await loadReports();
    } catch (error) { setOutput('report-admin-output', error.message); }
  });

  $('#btn-load-admin-locations')?.addEventListener('click', () => loadLocations('admin').catch(err => setOutput('geo-admin-output', err.message)));
  $('#admin-geo-search-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const data = formData(event.currentTarget);
      const loc = await searchLocation(data.mode, data.query, 'admin');
      setOutput('geo-admin-output', loc);
    } catch (error) { setOutput('geo-admin-output', error.message); }
  });
  $('#add-location-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const d = formData(event.currentTarget);
      const url = `${API.geolocation}/geolocation/add/${encode(d.name)}/${encode(d.description)}/${encode(d.address)}/${encode(d.latitude)}/${encode(d.longitude)}`;
      const response = await apiFetch(url, { method:'POST' });
      setOutput('geo-admin-output', response);
      await loadLocations('admin');
    } catch (error) { setOutput('geo-admin-output', error.message); }
  });
  $('#delete-location-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const d = formData(event.currentTarget);
      const response = await apiFetch(`${API.geolocation}/geolocation/${encode(d.location_id)}`, { method:'DELETE' });
      setOutput('geo-admin-output', response);
      await loadLocations('admin');
    } catch (error) { setOutput('geo-admin-output', error.message); }
  });

  $('#btn-load-coupons')?.addEventListener('click', () => loadCoupons().catch(err => setOutput('coupon-admin-output', err.message)));
  $('#btn-seed-coupons')?.addEventListener('click', () => seedCoupons().catch(err => setOutput('coupon-admin-output', err.message)));
  $('#create-coupon-form')?.addEventListener('submit', event => {
    event.preventDefault();
    createCouponFromForm(formData(event.currentTarget)).catch(err => setOutput('coupon-admin-output', err.message));
  });
  $('#coupon-filter-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const d = formData(event.currentTarget);
      const value = d.filter_value || '';
      const paths = {
        'all': '/coupons',
        'code': `/coupons/code/${encode(value)}`,
        'creation-date': `/coupons/creation-date/${encode(value)}`,
        'expiration-date': `/coupons/expiration-date/${encode(value)}`,
        'expired': '/coupons/expired',
        'valid': '/coupons/valid',
        'enabled': '/coupons/enabled',
        'disabled': '/coupons/disabled',
        'search': `/coupons/search/${encode(value)}`,
        'happy-birthday': '/coupons/happy-birthday',
        'referred': '/coupons/referred',
        'last': `/coupons/last/${encode(value)}`
      };
      const response = await apiFetch(`${API.coupon}${paths[d.filter_type]}`);
      renderCouponTable(Array.isArray(response) ? response : [response].filter(Boolean));
      setOutput('coupon-admin-output', response);
    } catch (error) { setOutput('coupon-admin-output', error.message); }
  });
  $('#coupon-code-action-form')?.addEventListener('submit', event => {
    event.preventDefault();
    const d = formData(event.currentTarget);
    runCouponCodeAction(d.coupon_code, d.action).catch(err => setOutput('coupon-admin-output', err.message));
  });
  $('#coupon-search-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const d = formData(event.currentTarget);
      const response = await apiFetch(`${API.coupon}/coupons/search/${encode(d.text)}`);
      renderCouponTable(Array.isArray(response) ? response : []);
      setOutput('coupon-admin-output', response);
    } catch (error) { setOutput('coupon-admin-output', error.message); }
  });
  $('#btn-load-users-coupons')?.addEventListener('click', async () => {
    try { setOutput('users-coupons-output', await apiFetch(`${API.coupon}/users/coupons/all`)); }
    catch (error) { setOutput('users-coupons-output', error.message); }
  });

  $('#email-template-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const d = formData(event.currentTarget);
      const config = buildEmailPayload(d.template, d.correo_institu, d.primer_nomb);
      const response = await apiFetch(`${API.email}${config.endpoint}`, {
        method:'POST',
        headers:{ 'X-API-Key': d.api_key, 'X-Correlation-ID': `front-${Date.now()}` },
        body: config.body
      });
      setOutput('email-admin-output', response);
    } catch (error) { setOutput('email-admin-output', error.message); }
  });

  $('#btn-render-endpoints')?.addEventListener('click', renderEndpointMatrix);
  $('#manual-request-form')?.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const d = formData(event.currentTarget);
      const opts = { method: d.method };
      if (d.body?.trim()) opts.body = JSON.parse(d.body);
      const response = await apiFetch(d.url, opts);
      setOutput('manual-output', response);
    } catch (error) { setOutput('manual-output', error.message); }
  });

  loadReports().catch(() => {});
  loadLocations('admin').catch(() => {});
  loadCoupons().catch(() => {});
}

initShared();
if (page === 'home') initHome();
if (page === 'user') initUser();
if (page === 'admin') initAdmin();
