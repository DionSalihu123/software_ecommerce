const API = {
  user: 'http://localhost:8000',
  product: 'http://localhost:8001',
  order: 'http://localhost:8002',
};

const state = {
  token: localStorage.getItem('ecom_token') || null,
  user: null,
};

const elements = {
  authStatus: document.getElementById('authStatus'),
  currentUser: document.getElementById('currentUser'),
  currentUserName: document.getElementById('currentUserName'),
  messageBox: document.getElementById('messageBox'),
  registerForm: document.getElementById('registerForm'),
  loginForm: document.getElementById('loginForm'),
  logoutButton: document.getElementById('logoutButton'),
  createProductForm: document.getElementById('createProductForm'),
  loadProductsButton: document.getElementById('loadProductsButton'),
  productsList: document.getElementById('productsList'),
  createOrderForm: document.getElementById('createOrderForm'),
  loadOrdersButton: document.getElementById('loadOrdersButton'),
  ordersList: document.getElementById('ordersList'),
  payOrderForm: document.getElementById('payOrderForm'),
  completeOrderForm: document.getElementById('completeOrderForm'),
};

const statusMap = {
  loggedOut: 'Not logged in',
  loggedIn: 'Logged in',
};

function appendMessage(message, type = 'info') {
  const item = document.createElement('div');
  item.className = 'rounded-2xl px-4 py-3 text-sm';
  item.textContent = message;

  if (type === 'error') {
    item.classList.add('bg-rose-500/10', 'text-rose-200', 'border', 'border-rose-500/20');
  } else if (type === 'success') {
    item.classList.add('bg-emerald-500/10', 'text-emerald-200', 'border', 'border-emerald-500/20');
  } else {
    item.classList.add('bg-slate-800', 'text-slate-200', 'border', 'border-slate-700');
  }

  elements.messageBox.prepend(item);
  while (elements.messageBox.children.length > 10) {
    elements.messageBox.removeChild(elements.messageBox.lastChild);
  }
}

function setMessage(message, type = 'info') {
  appendMessage(message, type);
}

function getAuthHeaders() {
  return state.token ? { Authorization: `Bearer ${state.token}` } : {};
}

async function fetchJson(url, options = {}) {
  const finalOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  const response = await fetch(url, finalOptions);
  const text = await response.text();
  const data = text ? JSON.parse(text) : null;

  if (!response.ok) {
    const message = data?.detail || data?.message || response.statusText;
    throw new Error(message);
  }

  return data;
}

function setAuthState() {
  const loggedIn = Boolean(state.token && state.user);
  elements.authStatus.textContent = loggedIn ? `${statusMap.loggedIn}` : `${statusMap.loggedOut}`;
  elements.authStatus.className = loggedIn
    ? 'rounded-full bg-emerald-500/10 px-3 py-1 text-[0.65rem] font-semibold uppercase tracking-[0.25em] text-emerald-200'
    : 'rounded-full bg-slate-700/70 px-3 py-1 text-[0.65rem] font-semibold uppercase tracking-[0.25em] text-slate-300';

  if (loggedIn) {
    elements.currentUser.classList.remove('hidden');
    elements.currentUserName.textContent = state.user.username;
  } else {
    elements.currentUser.classList.add('hidden');
    elements.currentUserName.textContent = '';
  }
}

function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(Number(value));
}

function buildStatusBadge(status) {
  const normalized = String(status || '').toLowerCase();
  const badgeStyles = {
    pending: 'bg-amber-500/10 text-amber-200 border border-amber-500/20',
    paid: 'bg-sky-500/10 text-sky-200 border border-sky-500/20',
    completed: 'bg-emerald-500/10 text-emerald-200 border border-emerald-500/20',
    cancelled: 'bg-rose-500/10 text-rose-200 border border-rose-500/20',
    failed: 'bg-red-500/10 text-red-200 border border-red-500/20',
  };

  const style = badgeStyles[normalized] || 'bg-slate-700/80 text-slate-300 border border-slate-700';
  return `<span class="inline-flex rounded-full px-3 py-1 text-xs font-semibold ${style}">${status || 'unknown'}</span>`;
}

function renderProducts(products) {
  if (!products || products.length === 0) {
    elements.productsList.innerHTML = '<div class="p-6 text-slate-400">No products found.</div>';
    return;
  }

  const rows = products
    .map(product => `
      <tr class="border-t border-slate-800/70 hover:bg-slate-900/80">
        <td class="whitespace-nowrap px-4 py-4 text-sm text-slate-200">${product.id}</td>
        <td class="px-4 py-4 text-sm text-slate-200">${product.name}</td>
        <td class="px-4 py-4 text-sm text-slate-300">${product.category}</td>
        <td class="px-4 py-4 text-sm text-slate-300">${formatCurrency(product.price)}</td>
        <td class="px-4 py-4 text-sm text-slate-300">${product.stock ?? '—'}</td>
        <td class="px-4 py-4 text-sm text-slate-300">${product.is_active ? 'Active' : 'Inactive'}</td>
      </tr>`)
    .join('');

  elements.productsList.innerHTML = `
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-slate-800 text-left">
        <thead class="border-b border-slate-800 bg-slate-950/90 text-slate-400">
          <tr>
            <th class="px-4 py-3 text-xs uppercase tracking-[0.18em]">ID</th>
            <th class="px-4 py-3 text-xs uppercase tracking-[0.18em]">Name</th>
            <th class="px-4 py-3 text-xs uppercase tracking-[0.18em]">Category</th>
            <th class="px-4 py-3 text-xs uppercase tracking-[0.18em]">Price</th>
            <th class="px-4 py-3 text-xs uppercase tracking-[0.18em]">Stock</th>
            <th class="px-4 py-3 text-xs uppercase tracking-[0.18em]">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">${rows}</tbody>
      </table>
    </div>`;
}

function renderOrders(orders) {
  if (!orders || orders.length === 0) {
    elements.ordersList.innerHTML = '<div class="p-6 text-slate-400">No orders available.</div>';
    return;
  }

  const rows = orders
    .map(order => {
      const productName = order.product?.name || `#${order.product_id}`;
      const statusLabel = buildStatusBadge(order.status);
      return `
        <tr class="border-t border-slate-800/70 hover:bg-slate-900/80">
          <td class="px-4 py-4 text-sm text-slate-200">${order.id}</td>
          <td class="px-4 py-4 text-sm text-slate-200">${productName}</td>
          <td class="px-4 py-4 text-sm text-slate-300">${order.quantity}</td>
          <td class="px-4 py-4 text-sm text-slate-300">${formatCurrency(order.total_amount)}</td>
          <td class="px-4 py-4 text-sm text-slate-300">${statusLabel}</td>
          <td class="px-4 py-4 text-sm text-slate-300">${order.payment_status || 'unknown'}</td>
        </tr>`;
    })
    .join('');

  elements.ordersList.innerHTML = `
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-slate-800 text-left">
        <thead class="border-b border-slate-800 bg-slate-950/90 text-slate-400">
          <tr>
            <th class="px-4 py-3 text-xs uppercase tracking-[0.18em]">Order</th>
            <th class="px-4 py-3 text-xs uppercase tracking-[0.18em]">Product</th>
            <th class="px-4 py-3 text-xs uppercase tracking-[0.18em]">Quantity</th>
            <th class="px-4 py-3 text-xs uppercase tracking-[0.18em]">Total</th>
            <th class="px-4 py-3 text-xs uppercase tracking-[0.18em]">Status</th>
            <th class="px-4 py-3 text-xs uppercase tracking-[0.18em]">Payment</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">${rows}</tbody>
      </table>
    </div>`;
}

async function loadCurrentUser() {
  if (!state.token) {
    state.user = null;
    setAuthState();
    return;
  }

  try {
    const user = await fetchJson(`${API.user}/me`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });

    state.user = user;
    setAuthState();
    setMessage(`Logged in as ${user.username}.`, 'success');
  } catch (error) {
    state.user = null;
    setAuthState();
    setMessage('Unable to validate session. Please login again.', 'error');
  }
}

async function registerUser(event) {
  event.preventDefault();
  const username = document.getElementById('registerUsername').value.trim();
  const email = document.getElementById('registerEmail').value.trim();
  const password = document.getElementById('registerPassword').value;

  const data = await fetchJson(`${API.user}/users`, {
    method: 'POST',
    body: JSON.stringify({ username, email, password }),
  });

  setMessage(`User created: ${data.username}`, 'success');
  event.target.reset();
}

async function loginUser(event) {
  event.preventDefault();
  const email = document.getElementById('loginEmail').value.trim();
  const password = document.getElementById('loginPassword').value;

  const data = await fetchJson(`${API.user}/login`, {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });

  state.token = data.access_token;
  localStorage.setItem('ecom_token', state.token);
  await loadCurrentUser();
  event.target.reset();
  await loadOrders().catch(() => {});
}

function logoutUser() {
  state.token = null;
  state.user = null;
  localStorage.removeItem('ecom_token');
  setAuthState();
  setMessage('Logged out.', 'info');
}

async function createProduct(event) {
  event.preventDefault();
  const name = document.getElementById('productName').value.trim();
  const category = document.getElementById('productCategory').value.trim();
  const price = document.getElementById('productPrice').value.trim();
  const description = document.getElementById('productDescription').value.trim();

  const data = await fetchJson(`${API.product}/products/`, {
    method: 'POST',
    body: JSON.stringify({ name, category, price, description }),
  });

  setMessage(`Product created: ${data.name} (#${data.id}).`, 'success');
  event.target.reset();
  await loadProducts();
}

async function loadProducts() {
  const data = await fetchJson(`${API.product}/products/`, { method: 'GET' });
  renderProducts(data);
  setMessage(`Loaded ${data.length} products.`, 'info');
}

async function createOrder(event) {
  event.preventDefault();
  if (!state.token) throw new Error('Login required to create orders.');

  const product_id = Number(document.getElementById('orderProductId').value);
  const quantity = Number(document.getElementById('orderQuantity').value) || 1;

  const data = await fetchJson(`${API.order}/orders/`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ product_id, quantity }),
  });

  setMessage(`Order created (#${data.id}) for product ${data.product_id}.`, 'success');
  event.target.reset();
  await loadOrders();
}

async function loadOrders() {
  if (!state.token) {
    elements.ordersList.innerHTML = '<div class="p-6 text-slate-400">Login to view your orders.</div>';
    return [];
  }

  const data = await fetchJson(`${API.order}/me/orders`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  renderOrders(data);
  setMessage(`Loaded ${data.length} orders.`, 'info');
  return data;
}

async function payOrder(event) {
  event.preventDefault();
  if (!state.token) throw new Error('Login required to pay orders.');

  const orderId = Number(document.getElementById('payOrderId').value);
  const data = await fetchJson(`${API.order}/orders/${orderId}/pay`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ payment_method: 'card' }),
  });

  setMessage(`Order #${orderId} paid successfully. Status: ${data.status}.`, 'success');
  document.getElementById('payOrderForm').reset();
  await loadOrders();
}

async function completeOrder(event) {
  event.preventDefault();
  if (!state.token) throw new Error('Login required to complete orders.');

  const orderId = Number(document.getElementById('completeOrderId').value);
  const data = await fetchJson(`${API.order}/orders/${orderId}/complete`, {
    method: 'POST',
    headers: getAuthHeaders(),
  });

  setMessage(`Order #${orderId} completed. License: ${data.license_key || 'none'}.`, 'success');
  document.getElementById('completeOrderForm').reset();
  await loadOrders();
}

async function safeAction(callback) {
  try {
    await callback();
  } catch (error) {
    setMessage(`Error: ${error.message}`, 'error');
  }
}

function setupEventListeners() {
  elements.registerForm.addEventListener('submit', event => safeAction(() => registerUser(event)));
  elements.loginForm.addEventListener('submit', event => safeAction(() => loginUser(event)));
  elements.logoutButton.addEventListener('click', () => safeAction(logoutUser));
  elements.createProductForm.addEventListener('submit', event => safeAction(() => createProduct(event)));
  elements.loadProductsButton.addEventListener('click', () => safeAction(loadProducts));
  elements.createOrderForm.addEventListener('submit', event => safeAction(() => createOrder(event)));
  elements.loadOrdersButton.addEventListener('click', () => safeAction(loadOrders));
  elements.payOrderForm.addEventListener('submit', event => safeAction(() => payOrder(event)));
  elements.completeOrderForm.addEventListener('submit', event => safeAction(() => completeOrder(event)));
}

async function init() {
  setAuthState();
  setupEventListeners();
  if (state.token) {
    await loadCurrentUser();
  }
  await loadProducts().catch(error => {
    setMessage(`Unable to load products: ${error.message}`, 'error');
  });
}

init();
