<template>
    <Navbar/>
    <div class="flex h-screen justify-center items-center">
        <div>
            <form @submit.prevent="handleSubmit" class="border-[2px] p-4 rounded-xl">
                <p class="text-red-400 animate-bounce" v-if="error['message']">{{ error.message }}</p>
                <div class="">
                    <label class="uppercase font-semibold">Email</label> <br>
                    <input class="border-[1px] p-2 rounded" type="email" v-model="email" required/>
                </div>
                <div class="pt-5">
                    <label class="uppercase font-semibold">Password</label> <br>
                    <input class="border-[1px] p-2 rounded" type="password" v-model="password" required/>
                </div>
                <div class="w-full flex justify-center items-center py-5">
                    <button class="w-full border-[1px] bg-green-300 hover:bg-green-500 p-2 rounded" type="submit">Login</button>
                </div>
                <p class="text-center">Not have an account?</p>
                <div class="w-full pt-3 flex justify-center text-center">
                    <router-link class="w-full bg-green-300 hover:bg-green-500 py-2" :to="{ name: 'register' }">Register</router-link>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import Navbar from './../components/Navbar.vue'
export default {
    name: "LoginView",
    components:{
        Navbar
    },
    data() {
        return {
            email: "rnaveen28102003@gmail.com",
            password: "test1234",
            error : {
                'message': ' '
            }
        };
    },
    watch:{
        email(){
            this.error = {}
        },
        password(){
            this.error = {}
        }
    },
    methods: {
        async handleSubmit() {
            try {
                console.log("Submitting form...");
                const resp = await fetch("/api/login", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email: this.email, password: this.password })
                });

                const data = await resp.json();
                if (resp.ok) {
                    localStorage.setItem('token', data.access_token);
                    this.$store.commit('logged_in')
                    this.$router.push({ name: 'todos'})
                } else {
                    this.error.message = data.message
                }
            } catch (error) {
                console.error("Error during form submission:", error);
                alert("There was an error with the login request.");
            }
        }
    }
}
</script>

<style lang="">
</style>
