<template lang="">
      <Navbar/>
    <form @submit.prevent="add_task" style="display:flex; justify-content:center; gap:20px; padding:20px 0 20px 0">
        <input class="border-[1px] border-green-500 p-1 outline-none" v-model="new_task" type="text" :placeholder="new_task_placeholder" required/>
        <button type="submit" class="border-[1px] rounded p-2 hover:bg-green-400 uppercase">Add Task</button>
    </form>
    <div class="flex items-center justify-center gap-7">
        <button @click="page_no-=1" class="border-[1px] border-gray-500 p-2 rounded" :disabled="!previous_page">Previous</button>
        <p>Task Per page: </p>
        <!-- <input class="border-[1px] border-green-200 p-2" type="select" v-model="count_no" min="1" max="10"/> -->
        <select v-model="count_no">
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
            <option value="6">6</option>
            <option value="7">7</option>
            <option value="8">8</option>
            <option value="9">9</option>
            <option value="10">10</option>
        </select>
        <button @click="page_no+=1" class="border-[1px] border-gray-500 p-2 rounded" :disabled="!next_page">Next</button>
    </div>
    <div class="flex justify-center items-center" id="display_the_total_todos">
        <p v-if="total_todos">{{(page_no-1) * count_no + 1}} - {{ page_no*count_no }} of {{ total_todos }}</p>
    </div>
    <div id="todos">
        <div v-if="todos" id="singletodo">
            <TodoComponents v-for="(todo,index) in todos" :key="todo.id" :todo="todo" />
        </div>
        <div v-if="!todos">
            No Todos Found
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
            new_task_placeholder_sentences : ["Need to arrange a meeting", "Walk with the dog", "Say a good bye"],
            count_no: 10,
            previous_page: null,
            next_page: null,
            page_no: 1,
            total_todos: null
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
        }, 1500);
    },
    watch:{
        count_no(){
            // this.page_no = 1
            this.get_todos()
        },
        page_no(){
            this.get_todos()
        }
    },
    methods: {
        async get_todos(){
            var query = `/api/todo/?`
            if (this.page_no){
                query += `page_no=${this.page_no}`
                if (this.count_no) {
                    query += `&page_count=${this.count_no}`
                }
            }
            const resp = await fetch(`${query}`,{
                method:'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            })
            const data = await resp.json()
            this.todos = data.todos.data
            this.previous_page = data.todos.previous_page
            this.next_page = data.todos.next_page
            this.total_todos = data.todos.total
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