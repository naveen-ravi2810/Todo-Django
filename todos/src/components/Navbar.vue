<template lang="">
    <div style="display:flex; align-items:center; justify-content:space-between; padding:10px 30px 10px 30px; position: relative;">
        <div>TODO</div>
        <div v-if="!isLoading">
            <div v-if="token_details">
                <button @click="profile_option=!profile_option">{{ token_details.name }}</button>
                <ul v-if="profile_option" style="display:flex; flex-direction:column;position: absolute; top: 100%; right: 0; background: white; list-style: none; padding: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">
                    <router-link to="/todos">Todos</router-link>
                    <router-link to="/profile">Profile</router-link>
                    <button @click="handleLogout">Logout</button>
                </ul>
            </div>
            <div>
                <p v-if="!token_details">Welcome</p>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    name:'Navbar',
    data() {
        return {
            token_details : null,
            isLoading: true,
            profile_option: false
        }
    },
    created() {
        if(localStorage.getItem('token')){
            this.get_token_status()
        } else {
            this.isLoading = false
        }
    },
    methods: {
        async get_token_status(){
            const resp = await fetch("/api/token",{
                method:'GET',
                headers:{
                    'Authorization':`Bearer ${localStorage.getItem("token")}`
                }
            })
            const data = await resp.json()
            if(resp.ok){
                this.token_details = data.user
                this.isLoading = false
            } 
        },
        handleLogout(){
            localStorage.removeItem('token')
            this.$router.replace({name:'login'})
        }
    },
}
</script>
<style lang="">
    
</style>