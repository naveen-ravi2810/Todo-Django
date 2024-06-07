<template lang="">
    <div class="flex justify-center items-center w-full pt-20">
        <form class="border-[1px] border-green-600 p-4 w-1/2" @submit.prevent="handleSubmit">
            <div class="py-3 flex flex-col gap-3">
                <label class="font-semibold uppercase">First name</label>
                <input class="border-[1px] border-gray-500 p-2" type="text" autofocus v-model="first_name" required/>
            </div>
            <div class="py-3 flex flex-col gap-3">
                <label class="font-semibold uppercase">Last name</label>
                <input class="border-[1px] border-gray-500 p-2" type="text" v-model="last_name" required/>
            </div>
            <div class="py-3 flex flex-col gap-3">
                <label class="font-semibold uppercase">Email</label>
                <input class="border-[1px] border-gray-500 p-2" type="email" v-model="email" required/>
                <p class="text-red-500 animate-bounce" v-if="error['email']">{{ error.email[0] }}</p>
            </div>
            <div class="py-3 flex flex-col gap-3">
                <label class="font-semibold uppercase">Phone</label>
                <input class="border-[1px] border-gray-500 p-2" type="tel" v-model="phone" required/>
            </div>
            <div class="py-3 flex flex-col gap-3">
                <label class="font-semibold uppercase">Password</label>
                <input class="border-[1px] border-gray-500 p-2" type="password" v-model="password" required/>
            </div>
            <div class="py-3 flex flex-col gap-3">
                <label class="font-semibold uppercase">Re-Enter Password</label>
                <input class="border-[1px] border-gray-500 p-2" type="password" v-model="re_enter_password" required/>
                <p class="text-red-500 animate-bounce" v-if="error['password']">{{ error.password }}</p>
            </div>
            <div class=w-full>
                <button class="w-full bg-green-500 py-2" type="submit">Register</button>
            </div>
            <div class="w-full flex justify-center pt-3">
                <p class="">Already have an account?</p>
            </div>
            <div class="w-full pt-3 flex justify-center text-center">
                <router-link class="w-full bg-green-500 py-2" :to="{name:'login'}">Login</router-link>
            </div>
        </form>
    </div>
</template>
<script>
export default {
    name:'RegisterView',
    data(){
        return{
            first_name : "",
            last_name : "",
            email : "",
            phone : "",
            password : "",
            re_enter_password : "",
            error : {}
        }
    },
    watch:{
        password(){
            this.error.password=""
        },
        re_enter_password(){
            this.error.password=""
        },
        email(){
            this.error.email=""
        }
    },
    methods:{
        async handleSubmit(){
            try{
                if (this.password != this.re_enter_password){
                    this.error.password = "Password does not match"
                    return 
                }
                const resp = await fetch("/api/register",{
                    method:'POST',
                    headers:{
                        'Content-Type':'application/json'
                    },
                    body:JSON.stringify({
                        // fields = ["first_name", "last_name", "password", "email", "phone"]
                        'first_name' : this.first_name,
                        'last_name' : this.last_name,
                        'password' : this.password,
                        'email' : this.email,
                        'phone' : this.phone,
                    })
                })
                if(resp.ok){
                    const login_resp = await fetch("/api/login",{
                        method:'POST',
                        headers:{
                            'Content-Type':'application/json'
                        },
                        body:JSON.stringify({
                            'email':this.email,
                            'password':this.password
                        })
                    })
                    if (login_resp.ok){
                        const data = await login_resp.json()
                        localStorage.setItem('token', data.access_token)
                        this.$router.push({name:'todos'})
                    }
                } else{
                    const data = await resp.json()
                    this.error = data.message
                }
            } catch {
                alert("Sorry this is an erroor")
            }
        }
    }
}
</script>
<style lang="">
    
</style>