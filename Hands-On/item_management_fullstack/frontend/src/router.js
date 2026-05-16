import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import Dashboard from './views/Dashboard.vue'
import Products from './views/Products.vue'
import ProductForm from './views/ProductForm.vue'
import Categories from './views/Categories.vue'
import CategoryForm from './views/CategoryForm.vue'
import Customers from './views/Customers.vue'
import CustomerForm from './views/CustomerForm.vue'
import Orders from './views/Orders.vue'
import OrderDetail from './views/OrderDetail.vue'
import OrderCreate from './views/OrderCreate.vue'

const routes = [
  { path: '/login', component: Login },
  { path: '/', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/products', component: Products, meta: { requiresAuth: true } },
  { path: '/products/new', component: ProductForm, meta: { requiresAuth: true } },
  { path: '/products/:id/edit', component: ProductForm, meta: { requiresAuth: true } },
  { path: '/categories', component: Categories, meta: { requiresAuth: true } },
  { path: '/categories/new', component: CategoryForm, meta: { requiresAuth: true } },
  { path: '/categories/:id/edit', component: CategoryForm, meta: { requiresAuth: true } },
  { path: '/customers', component: Customers, meta: { requiresAuth: true } },
  { path: '/customers/new', component: CustomerForm, meta: { requiresAuth: true } },
  { path: '/customers/:id/edit', component: CustomerForm, meta: { requiresAuth: true } },
  { path: '/orders', component: Orders, meta: { requiresAuth: true } },
  { path: '/orders/new', component: OrderCreate, meta: { requiresAuth: true } },
  { path: '/orders/:id', component: OrderDetail, meta: { requiresAuth: true } },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    try {
      const res = await fetch('/api/auth/me', { credentials: 'include' })
      if (!res.ok) return next('/login')
    } catch {
      return next('/login')
    }
  }
  next()
})

export default router
