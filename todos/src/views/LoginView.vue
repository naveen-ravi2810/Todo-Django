<template>
    <div>
        <form @submit.prevent="handleSubmit">
            <div>
                <label>Email</label>
                <input type="email" v-model="email" required/>
            </div>
            <div>
                <label>Password</label>
                <input type="password" v-model="password" required/>
            </div>
            <div>
                <button type="submit">Login</button>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    name: "LoginView",
    data() {
        return {
            email: "rnaveen28102003@gmail.com",
            password: "test1234"
        };
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
                    alert(data.message);
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
