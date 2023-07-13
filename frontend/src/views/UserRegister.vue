<template>
    <div>
      <h1>Register</h1>
      <input v-model="name" type="text" placeholder="Name">
      <input v-model="email" type="email" placeholder="Email">
      <input v-model="password" type="password" placeholder="Password">
      <button @click="register">Register</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        name: '',
        email: '',
        password: ''
      }
    },
    methods: {
      async register() {
        try {
          const response = await axios.post('http://localhost:8000/users', {
            name: this.name,
            email: this.email,
            password: this.password
          })
          this.$router.push('/dashboard')
        } catch (error) {
          console.log(error)
        }
      }
    }
  }
  </script>
  