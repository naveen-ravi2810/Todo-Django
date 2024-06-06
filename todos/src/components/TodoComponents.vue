<template>
    <div v-if="is_active" :class="['p-[10px]', 'mt-[10px]', 'flex', 'justify-between', 'items-center', localTodo.status ? 'bg-green-500' : 'bg-red-300']">
        <div>
            <p>{{ localTodo.task }}</p>
            <p>{{ localTodo.created_on.slice(0,10) }}</p>
            <p>{{  localTodo.created_on.slice(11,19) }}</p>
        </div>
        <div class="flex flex-col justify-center">
            <button class="border-[1px] py-1 px-2 rounded" @click="delete_task">Delete Task</button> <br>
            <button class="border-[1px] py-1 px-2 rounded" @click="update_status">{{ localTodo.status ? 'Completed' : 'Not Completed' }}</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TodoComponent',
    props: {
        todo: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            localTodo: { ...this.todo },
            is_active: true
        };
    },
    methods: {
        async update_status() {
            try {
                const resp = await fetch(`/api/todo/${this.localTodo.id}`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                if (resp.ok) {
                    this.localTodo.status = !this.localTodo.status;
                } else {
                    alert('Not changed');
                }
            } catch (error) {
                console.error('Error updating status:', error);
                alert('An error occurred');
            }
        },
        async delete_task(){
            try{
                const resp = await fetch(`/api/todo/${this.localTodo.id}`,{
                    method:'DELETE',
                    headers:{
                        'Authorization':`Bearer ${localStorage.getItem('token')}`
                    }
                })
                if(resp.ok){
                    this.is_active = false
                }
                else{
                    alert("cannot delete this task")
                }
            } catch{
                alert("An error Occured")
            }
        }
    },
};
</script>

<style scoped>

.completedtask {
    background-color: greenyellow;
}
.notcompletedtask {
    background-color: lightcoral;
}
</style>
