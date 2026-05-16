<template>
  <div>
    <h2><i class="fas fa-shopping-cart"></i> Orders</h2>
    <div style="margin:1rem 0;"><router-link to="/orders/new" class="btn btn-primary"><i class="fas fa-plus"></i> New Order</router-link></div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="card">
      <div class="card-header"><i class="fas fa-table"></i> All Orders ({{ total }})</div>
      <div class="card-body" style="padding:0;">
        <table class="table">
          <thead><tr><th>#</th><th>Customer</th><th>Date</th><th>Items</th><th>Total</th><th>Status</th><th></th></tr></thead>
          <tbody>
            <tr v-for="o in orders" :key="o.id">
              <td>#{{ o.id }}</td><td>{{ o.customer_name }}</td>
              <td>{{ o.order_date?.slice(0,10) }}</td><td>{{ o.items?.length || 0 }}</td>
              <td>${{ o.total_amount.toFixed(2) }}</td>
              <td><span class="badge">{{ o.status }}</span></td>
              <td><router-link :to="'/orders/'+o.id" class="btn btn-sm btn-primary"><i class="fas fa-eye"></i></router-link></td>
            </tr>
            <tr v-if="!orders.length"><td colspan="7" class="text-center">No orders yet.</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button class="btn btn-sm" :class="page<=1?'btn-disabled':''" :disabled="page<=1" @click="goPage(page-1)">&larr; Previous</button>
      <span v-for="n in totalPages" :key="n" class="btn btn-sm" :class="n===page?'btn-active':''" @click="goPage(n)">{{ n }}</span>
      <button class="btn btn-sm" :class="page>=totalPages?'btn-disabled':''" :disabled="page>=totalPages" @click="goPage(page+1)">Next &rarr;</button>
    </div>
  </div>
</template>

<script>
import api from '../api.js'
export default {
  data() { return { orders: [], total: 0, page: 1, totalPages: 1, loading: true } },
  async created() { await this.load() },
  methods: {
    async load() {
      this.loading = true
      try {
        const res = await api.orders({ page: this.page })
        this.orders = res.orders; this.total = res.total; this.totalPages = res.total_pages
      } catch (e) { alert(e.message) }
      finally { this.loading = false }
    },
    goPage(n) { this.page = n; this.load() },
  },
}
</script>
