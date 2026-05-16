<template>
  <div v-if="loading" class="loading">Loading...</div>
  <div v-else-if="order">
    <h2><i class="fas fa-file-invoice"></i> Order #{{ order.id }}</h2>

    <div class="card">
      <div class="card-header"><i class="fas fa-info-circle"></i> Order Info</div>
      <div class="card-body">
        <table class="table">
          <tr><td><strong>Customer</strong></td><td>{{ order.customer_name }}</td></tr>
          <tr><td><strong>Date</strong></td><td>{{ order.order_date?.slice(0,10) }}</td></tr>
          <tr><td><strong>Status</strong></td>
            <td>
              <span class="badge">{{ order.status }}</span>
              <select v-model="newStatus" class="btn-sm" style="width:auto;margin-left:0.5rem;">
                <option value="pending">pending</option>
                <option value="completed">completed</option>
                <option value="cancelled">cancelled</option>
              </select>
              <button class="btn btn-sm btn-primary" @click="updateStatus" style="margin-left:0.3rem;">Update</button>
            </td>
          </tr>
          <tr><td><strong>Total</strong></td><td><strong>${{ order.total_amount.toFixed(2) }}</strong></td></tr>
        </table>
      </div>
    </div>

    <div class="card">
      <div class="card-header"><i class="fas fa-list"></i> Items</div>
      <div class="card-body" style="padding:0;">
        <table class="table">
          <thead><tr><th>Product</th><th>Unit Price</th><th>Quantity</th><th>Subtotal</th></tr></thead>
          <tbody>
            <tr v-for="item in order.items" :key="item.id">
              <td>{{ item.product_name || 'Product #'+item.product_id }}</td>
              <td>${{ item.unit_price.toFixed(2) }}</td>
              <td>{{ item.quantity }}</td>
              <td>${{ (item.unit_price * item.quantity).toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <router-link to="/orders" class="btn btn-secondary"><i class="fas fa-arrow-left"></i> Back to Orders</router-link>
  </div>
</template>

<script>
import api from '../api.js'
export default {
  data() { return { order: null, loading: true, newStatus: 'pending' } },
  async created() {
    try {
      this.order = await api.order(this.$route.params.id)
      this.newStatus = this.order.status
    } catch (e) { alert(e.message) }
    finally { this.loading = false }
  },
  methods: {
    async updateStatus() {
      try {
        this.order = await api.updateOrderStatus(this.$route.params.id, this.newStatus)
      } catch (e) { alert(e.message) }
    },
  },
}
</script>
