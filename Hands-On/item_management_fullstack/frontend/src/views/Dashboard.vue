<template>
  <div>
    <h2><i class="fas fa-chart-pie"></i> Shop Dashboard</h2>
    <div v-if="loading" class="loading">Loading...</div>
    <template v-else-if="data">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin:1.5rem 0;">
        <div class="card" style="text-align:center;"><div class="card-header">Products</div><div class="card-body"><span style="font-size:2.5rem;font-weight:700;color:#2b9348;">{{ data.total_products }}</span></div></div>
        <div class="card" style="text-align:center;"><div class="card-header">Categories</div><div class="card-body"><span style="font-size:2.5rem;font-weight:700;color:#e9c46a;">{{ data.total_categories }}</span></div></div>
        <div class="card" style="text-align:center;"><div class="card-header">Customers</div><div class="card-body"><span style="font-size:2.5rem;font-weight:700;color:#2b9348;">{{ data.total_customers }}</span></div></div>
        <div class="card" style="text-align:center;"><div class="card-header">Orders</div><div class="card-body"><span style="font-size:2.5rem;font-weight:700;color:#145c32;">{{ data.total_orders }}</span></div></div>
        <div class="card" style="text-align:center;"><div class="card-header">Revenue</div><div class="card-body"><span style="font-size:2.5rem;font-weight:700;color:#2b9348;">${{ data.total_revenue.toFixed(2) }}</span></div></div>
        <div class="card" style="text-align:center;"><div class="card-header">Low Stock</div><div class="card-body"><span style="font-size:2.5rem;font-weight:700;color:#d62828;">{{ data.low_stock }}</span></div></div>
      </div>

      <div class="card">
        <div class="card-header"><i class="fas fa-clock"></i> Recent Orders</div>
        <div class="card-body" style="padding:0;">
          <table class="table">
            <thead><tr><th>#</th><th>Customer</th><th>Date</th><th>Total</th><th>Status</th><th></th></tr></thead>
            <tbody>
              <tr v-for="o in data.recent_orders" :key="o.id">
                <td>#{{ o.id }}</td><td>{{ o.customer_name }}</td>
                <td>{{ o.order_date?.slice(0,10) }}</td>
                <td>${{ o.total_amount.toFixed(2) }}</td>
                <td><span class="badge">{{ o.status }}</span></td>
                <td><router-link :to="'/orders/'+o.id" class="btn btn-sm btn-primary">View</router-link></td>
              </tr>
              <tr v-if="!data.recent_orders.length"><td colspan="6" class="text-center">No orders yet.</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div style="display:flex;gap:1rem;flex-wrap:wrap;">
        <router-link to="/products/new" class="btn btn-primary"><i class="fas fa-plus"></i> Add Product</router-link>
        <router-link to="/categories/new" class="btn btn-primary"><i class="fas fa-plus"></i> Add Category</router-link>
        <router-link to="/customers/new" class="btn btn-primary"><i class="fas fa-plus"></i> Add Customer</router-link>
        <router-link to="/orders/new" class="btn btn-primary"><i class="fas fa-plus"></i> New Order</router-link>
      </div>
    </template>
  </div>
</template>

<script>
import api from '../api.js'
export default {
  data() { return { data: null, loading: true } },
  async created() {
    try { this.data = await api.dashboard() }
    catch (e) { alert(e.message) }
    finally { this.loading = false }
  },
}
</script>
