<template>
    <div v-if="is_active" :class="{ completedtask: localTodo.status, notcompletedtask: !localTodo.status }" id="task-div">
        <div>
            <p>{{ localTodo.task }}</p>
            <p>{{ localTodo.created_on }}</p>
        </div>
        <div>
            <button @click="delete_task">Delete Task</button> <br>
            <button @click="update_status">{{ localTodo.status ? 'Completed' : 'Not Completed' }}</button>
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
#task-div {
    padding: 10px;
    margin: 10px 0;
    display: flex;
    justify-content: space-between;
}
.completedtask {
    background-color: greenyellow;
}
.notcompletedtask {
    background-color: lightcoral;
}
</style>
