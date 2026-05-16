<template>
  <div>
    <h2><i class="fas fa-tags"></i> Categories</h2>
    <div style="margin:1rem 0;"><router-link to="/categories/new" class="btn btn-primary"><i class="fas fa-plus"></i> Add Category</router-link></div>

    <div class="sort-controls">
      <span>Sort by:</span>
      <button class="btn btn-sm" :class="sort==='default'?'btn-active':''" @click="sort='default'; load()">Default</button>
      <button class="btn btn-sm" :class="sort==='name'?'btn-active':''" @click="sort='name'; load()">Name</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="card">
      <div class="card-header"><i class="fas fa-table"></i> All Categories ({{ total }})</div>
      <div class="card-body" style="padding:0;">
        <table class="table">
          <thead><tr><th>ID</th><th>Name</th><th>Description</th><th>Products</th><th>Actions</th></tr></thead>
          <tbody>
            <tr v-for="c in categories" :key="c.id">
              <td>{{ c.id }}</td><td>{{ c.name }}</td><td>{{ c.description || '&mdash;' }}</td>
              <td>{{ c.product_count }}</td>
              <td>
                <router-link :to="'/categories/'+c.id+'/edit'" class="btn btn-warning btn-sm"><i class="fas fa-edit"></i></router-link>
                <button class="btn btn-danger btn-sm" @click="doDelete(c)"><i class="fas fa-trash-alt"></i></button>
              </td>
            </tr>
            <tr v-if="!categories.length"><td colspan="5" class="text-center">No categories yet.</td></tr>
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
  data() { return { categories: [], total: 0, page: 1, totalPages: 1, sort: 'default', loading: true } },
  async created() { await this.load() },
  methods: {
    async load() {
      this.loading = true
      try {
        const res = await api.categories({ sort: this.sort, page: this.page })
        this.categories = res.categories; this.total = res.total; this.totalPages = res.total_pages
      } catch (e) { alert(e.message) }
      finally { this.loading = false }
    },
    goPage(n) { this.page = n; this.load() },
    async doDelete(c) {
      if (!confirm(`Delete category "${c.name}"?`)) return
      await api.deleteCategory(c.id); this.load()
    },
  },
}
</script>
