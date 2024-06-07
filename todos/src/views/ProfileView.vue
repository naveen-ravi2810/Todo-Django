<template lang="">
    <div>
        <Navbar/>
        <div class="container mx-auto mt-8">
            <table v-if="user" class="min-w-full bg-white border border-gray-200">
                <tbody>
                    <tr v-for="(value, key) in user" :key="key">
                        <td class="py-2 px-4 border-b">{{ key }}</td>
                        <td class="py-2 px-4 border-b">{{ value }}</td>
                    </tr>
                </tbody>
            </table>
            <div v-else class="text-center text-gray-500">
                Loading...
            </div>
        </div>
    </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'

export default {
    name: 'ProfileView',
    components: {
        Navbar
    },
    data() {
        return {
            user: null
        }
    },
    created() {
        this.get_user_profile()
    },
    methods: {
        async get_user_profile() {
            const resp = await fetch("/api/profile", {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            })
            const data = await resp.json()
            if (resp.ok) {
                this.user = data
            } else {
                alert(resp.statusText)
            }
        }
    }
}
</script>

<style lang="">
</style>
