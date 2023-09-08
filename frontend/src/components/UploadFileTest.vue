<template>
    <div class="test-upload">
        <input type="file" @change="onFileSelected">
        <button @click="onUpload">Upload</button>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            selectedFile: null
        }
    },
    methods: {
        onFileSelected(event) {
            this.selectedFile = event.target.files[0]
            console.log(this.selectedFile)
            
        },
        onUpload() {
            const fd = new FormData();
            fd.append('file', this.selectedFile)

            axios.post('http://localhost:8008/predict',fd)
             .then(res => {
                console.log(res)
             })
        }
    }
}
</script>

<style>

</style>