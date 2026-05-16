<template>
  <div>
    <h2><i class="fas fa-users"></i> Customers</h2>
    <div style="margin:1rem 0;"><router-link to="/customers/new" class="btn btn-primary"><i class="fas fa-plus"></i> Add Customer</router-link></div>

    <div class="sort-controls">
      <span>Sort by:</span>
      <button v-for="s in sortOptions" :key="s.key" class="btn btn-sm" :class="sort===s.key?'btn-active':''" @click="sort=s.key; load()">{{ s.label }}</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="card">
      <div class="card-header"><i class="fas fa-table"></i> All Customers ({{ total }})</div>
      <div class="card-body" style="padding:0;">
        <table class="table">
          <thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Orders</th><th>Actions</th></tr></thead>
          <tbody>
            <tr v-for="c in customers" :key="c.id">
              <td>{{ c.id }}</td><td>{{ c.name }}</td><td>{{ c.email }}</td><td>{{ c.phone || '&mdash;' }}</td>
              <td>{{ c.order_count }}</td>
              <td>
                <router-link :to="'/customers/'+c.id+'/edit'" class="btn btn-warning btn-sm"><i class="fas fa-edit"></i></router-link>
                <button class="btn btn-danger btn-sm" @click="doDelete(c)"><i class="fas fa-trash-alt"></i></button>
              </td>
            </tr>
            <tr v-if="!customers.length"><td colspan="6" class="text-center">No customers yet.</td></tr>
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
  data() {
    return {
      customers: [], total: 0, page: 1, totalPages: 1, sort: 'default', loading: true,
      sortOptions: [{key:'default',label:'Default'},{key:'name',label:'Name'},{key:'email',label:'Email'}],
    }
  },
  async created() { await this.load() },
  methods: {
    async load() {
      this.loading = true
      try {
        const res = await api.customers({ sort: this.sort, page: this.page })
        this.customers = res.customers; this.total = res.total; this.totalPages = res.total_pages
      } catch (e) { alert(e.message) }
      finally { this.loading = false }
    },
    goPage(n) { this.page = n; this.load() },
    async doDelete(c) {
      if (!confirm(`Delete customer "${c.name}"? This will also delete their orders.`)) return
      await api.deleteCustomer(c.id); this.load()
    },
  },
}
</script>
