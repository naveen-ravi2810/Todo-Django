<template lang="">
    <div>
        <form @submit.prevent="handleSubmit">
            <div>
                <label>First name</label>
                <input type="text" v-model="first_name" required/>
            </div>
            <div>
                <label>Last name</label>
                <input type="text" v-model="last_name" required/>
            </div>
            <div>
                <label>Email</label>
                <input type="email" v-model="email" required/>
            </div>
            <div>
                <label>Phone</label>
                <input type="number" v-model="phone" required/>
            </div>
            <div>
                <label>Password</label>
                <input type="password" v-model="password" required/>
            </div>
            <div>
                <label>Re-Enter Password</label>
                <input type="password" v-model="re_enter_password" required/>
            </div>
            <div>
                <button type="submit">Register</button>
            </div>
        </form>
        <router-link :to="{name:'login'}">Login</router-link>
    </div>
</template>
<script>
export default {
    name:'RegisterView',
    data(){
        return{
            first_name : "test",
            last_name : "user",
            email : "testuser@gmail.com",
            phone : "3456789012",
            password : "test1234",
            re_enter_password : "test1234",
        }
    },methods:{
        async handleSubmit(){
            try{
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
                    alert("An error occured")
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