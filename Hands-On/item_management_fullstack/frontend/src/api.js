const BASE = ''

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

export default {
  // Auth
  login(username, password) {
    return request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })
  },
  logout() {
    return request('/api/auth/logout', { method: 'POST' })
  },
  me() {
    return request('/api/auth/me')
  },

  // Dashboard
  dashboard() {
    return request('/api/dashboard')
  },

  // Products
  products(params = {}) {
    const q = new URLSearchParams(params).toString()
    return request(`/api/products?${q}`)
  },
  product(id) {
    return request(`/api/products/${id}`)
  },
  createProduct(data) {
    return request('/api/products', { method: 'POST', body: JSON.stringify(data) })
  },
  updateProduct(id, data) {
    return request(`/api/products/${id}`, { method: 'PUT', body: JSON.stringify(data) })
  },
  patchProduct(id, data) {
    return request(`/api/products/${id}`, { method: 'PATCH', body: JSON.stringify(data) })
  },
  deleteProduct(id) {
    return request(`/api/products/${id}`, { method: 'DELETE' })
  },

  // Categories
  categories(params = {}) {
    const q = new URLSearchParams(params).toString()
    return request(`/api/categories?${q}`)
  },
  createCategory(data) {
    return request('/api/categories', { method: 'POST', body: JSON.stringify(data) })
  },
  updateCategory(id, data) {
    return request(`/api/categories/${id}`, { method: 'PUT', body: JSON.stringify(data) })
  },
  deleteCategory(id) {
    return request(`/api/categories/${id}`, { method: 'DELETE' })
  },

  // Customers
  customers(params = {}) {
    const q = new URLSearchParams(params).toString()
    return request(`/api/customers?${q}`)
  },
  createCustomer(data) {
    return request('/api/customers', { method: 'POST', body: JSON.stringify(data) })
  },
  updateCustomer(id, data) {
    return request(`/api/customers/${id}`, { method: 'PUT', body: JSON.stringify(data) })
  },
  deleteCustomer(id) {
    return request(`/api/customers/${id}`, { method: 'DELETE' })
  },

  // Orders
  orders(params = {}) {
    const q = new URLSearchParams(params).toString()
    return request(`/api/orders?${q}`)
  },
  order(id) {
    return request(`/api/orders/${id}`)
  },
  createOrder(data) {
    return request('/api/orders', { method: 'POST', body: JSON.stringify(data) })
  },
  updateOrderStatus(id, status) {
    return request(`/api/orders/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    })
  },
}
