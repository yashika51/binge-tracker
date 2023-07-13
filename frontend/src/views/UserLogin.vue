<template>
    <div>
      <h1>Login</h1>
      <input v-model="email" type="email" placeholder="Email">
      <input v-model="password" type="password" placeholder="Password">
      <button @click="login">Login</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        email: '',
        password: ''
      }
    },
    methods: {
      async login() {
        try {
          const response = await axios.post('http://localhost:8000/users/login', {
            username: this.email,
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
  