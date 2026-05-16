<template>
  <div>
    <h2><i class="fas fa-box"></i> Products</h2>

    <div class="card">
      <div class="card-header"><i class="fas fa-filter"></i> Search &amp; Filter</div>
      <div class="card-body">
        <div class="d-flex gap-2" style="flex-wrap:wrap;">
          <div style="flex:2;"><label>Search</label><input v-model="filters.q" placeholder="Name or description..." /></div>
          <div style="flex:1;"><label>Min price</label><input v-model.number="filters.min_price" type="number" /></div>
          <div style="flex:1;"><label>Max price</label><input v-model.number="filters.max_price" type="number" /></div>
          <div style="flex:1;">
            <label>Category</label>
            <select v-model.number="filters.category_id">
              <option :value="0">All</option>
              <option v-for="c in cats" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div style="align-self:flex-end;">
            <button class="btn btn-primary" @click="load"><i class="fas fa-search"></i> Search</button>
            <button class="btn btn-secondary" @click="resetFilters"><i class="fas fa-undo-alt"></i> Reset</button>
          </div>
        </div>
      </div>
    </div>

    <div style="margin:1rem 0;">
      <router-link to="/products/new" class="btn btn-primary"><i class="fas fa-plus"></i> Add Product</router-link>
    </div>

    <div class="sort-controls">
      <span>Sort by:</span>
      <button v-for="s in sortOptions" :key="s.key" class="btn btn-sm" :class="filters.sort===s.key?'btn-active':''" @click="filters.sort=s.key; load()">{{ s.label }}</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <template v-else>
      <div class="card">
        <div class="card-header"><i class="fas fa-table"></i> Products ({{ total }})</div>
        <div class="card-body" style="padding:0;">
          <table class="table">
            <thead><tr><th>ID</th><th>Name</th><th>Category</th><th>Price</th><th>Stock</th><th>Actions</th></tr></thead>
            <tbody>
              <tr v-for="p in products" :key="p.id">
                <td>{{ p.id }}</td><td>{{ p.name }}</td><td>{{ p.category_name || '&mdash;' }}</td>
                <td>${{ p.price.toFixed(2) }}</td>
                <td><span :style="{color:p.stock<5?'#d62828':'inherit',fontWeight:p.stock<5?700:'inherit'}">{{ p.stock }}</span></td>
                <td>
                  <router-link :to="'/products/'+p.id+'/edit'" class="btn btn-warning btn-sm"><i class="fas fa-edit"></i></router-link>
                  <button class="btn btn-danger btn-sm" @click="doDelete(p)"><i class="fas fa-trash-alt"></i></button>
                </td>
              </tr>
              <tr v-if="!products.length"><td colspan="6" class="text-center">No products found.</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="totalPages > 1" class="pagination">
        <button class="btn btn-sm" :class="page<=1?'btn-disabled':''" :disabled="page<=1" @click="goPage(page-1)">&larr; Previous</button>
        <span v-for="n in totalPages" :key="n" class="btn btn-sm" :class="n===page?'btn-active':''" @click="goPage(n)">{{ n }}</span>
        <button class="btn btn-sm" :class="page>=totalPages?'btn-disabled':''" :disabled="page>=totalPages" @click="goPage(page+1)">Next &rarr;</button>
      </div>
    </template>
  </div>
</template>

<script>
import api from '../api.js'
export default {
  data() {
    return {
      products: [], cats: [], total: 0, page: 1, totalPages: 1, loading: true,
      filters: { sort: 'default', q: '', min_price: null, max_price: null, category_id: 0 },
      sortOptions: [
        { key: 'default', label: 'Default' }, { key: 'name', label: 'Name' },
        { key: 'price', label: 'Price' }, { key: 'stock', label: 'Stock' },
      ],
    }
  },
  async created() { await this.load() },
  methods: {
    async load() {
      this.loading = true
      try {
        const params = { sort: this.filters.sort, page: this.page }
        if (this.filters.q) params.q = this.filters.q
        if (this.filters.min_price) params.min_price = this.filters.min_price
        if (this.filters.max_price) params.max_price = this.filters.max_price
        if (this.filters.category_id) params.category_id = this.filters.category_id
        const res = await api.products(params)
        this.products = res.products
        this.total = res.total
        this.totalPages = res.total_pages
        this.cats = res.categories || []
      } catch (e) { alert(e.message) }
      finally { this.loading = false }
    },
    goPage(n) { this.page = n; this.load() },
    resetFilters() {
      this.filters = { sort: 'default', q: '', min_price: null, max_price: null, category_id: 0 }
      this.page = 1; this.load()
    },
    async doDelete(p) {
      if (!confirm(`Delete "${p.name}"?`)) return
      await api.deleteProduct(p.id)
      this.load()
    },
  },
}
</script>
