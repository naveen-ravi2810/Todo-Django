<template lang="">
    <form @submit.prevent="add_task">
        <input v-model="new_task" type="text" placeholder="enter new task" required/>
        <button type="submit">Add Task</button>
    </form>
    <div id="todos">
        <div id="singletodo">
            <TodoComponents v-for="(todo,index) in todos" :key="todo.id" :todo="todo" />
        </div>
    </div>
</template>
<script>
import TodoComponents from '@/components/TodoComponents.vue';
export default {
    name:'TodoView',
    components:{
        TodoComponents
    },
    data() {
        return {
            todos: null,
            new_task : ""
        }
    },
    created(){
        this.get_todos()
    },
    methods: {
        async get_todos(){
            const resp = await fetch("/api/todo/",{
                method:'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            })
            const data = await resp.json()
            this.todos = data.todos
        },
        async add_task(){
            try{
                const resp = await fetch("/api/todo/",{
                    method:"POST",
                    headers :{
                        'Authorization':`Bearer ${localStorage.getItem('token')}`,
                        'Content-Type':'application/json'
                    },
                    body:JSON.stringify({task:this.new_task})
                })
                if(resp.ok){
                    const data = await resp.json()
                    this.todos = [...this.todos, {
                        'task':this.new_task,
                        'status':false,
                        'created_on': await data.todo.created_on,
                        'id':await data.todo.id
                    }]
                } else{
                    alert("An error occured")
                }
            } catch {
                alert("An error Occured")
            }
        }
    }
}
</script>

<style scoped>
    #todos{
        display: flex;
        justify-content: center;
        width: 100%;
    }
    #singletodo{
        width: 50%;
    }
</style>