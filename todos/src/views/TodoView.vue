<template lang="">
      <Navbar/>
    <form @submit.prevent="add_task" style="display:flex; justify-content:center; gap:20px; padding:20px 0 20px 0">
        <input class="border-[1px] border-green-500 p-1 outline-none" v-model="new_task" type="text" :placeholder="new_task_placeholder" required/>
        <button type="submit" class="border-[1px] rounded p-2 hover:bg-green-400 uppercase">Add Task</button>
    </form>
    <div id="todos">
        <div id="singletodo">
            <TodoComponents v-for="(todo,index) in todos" :key="todo.id" :todo="todo" />
        </div>
    </div>
</template>
<script>
import TodoComponents from '@/components/TodoComponents.vue';
import Navbar from '@/components/Navbar.vue'

export default {
    name:'TodoView',
    components:{
        TodoComponents, Navbar
    },
    data() {
        return {
            todos: null,
            new_task : "",
            new_task_placeholder : "Say a good bye",
            new_task_placeholder_sentences : ["Need to arrange a meeting", "Walk with the dog", "Say a good bye"]
        }
    },
    created() {
        if (localStorage.getItem('token')) {
            this.get_todos();
        } else {
            this.$router.replace({ name: 'login' });
        }
        let index = 0;
        this.placeholderInterval = setInterval(() => {
            this.new_task_placeholder = this.new_task_placeholder_sentences[index];
            index = (index + 1) % this.new_task_placeholder_sentences.length;
        }, 1000);
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
                    this.new_task = ""
                } else if(resp.status == 500){
                    alert("Server error")
                } else {
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