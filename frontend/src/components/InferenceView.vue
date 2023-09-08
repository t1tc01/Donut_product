<template>
  <div>
    <a-row>
        <a-col :span="12">
            <h1>Image Space</h1><br>
            <img id="preview-image">
        </a-col>
        <a-col :span="12">
            <p>Invoice Document parsing play ground</p>
            <p>Bạn có thể đăng hóa đơn của bạn ở bên dưới và xem các thông tin được trích xuất</p>
            <input type="file" @change="onFileSelected">
            <button @click="onUpload">Upload</button>  
            <div id="res-space">
                <h1 id="res-data-json-title"></h1>
                <p id="res-data-json"></p>
            </div>
            
        </a-col>
      </a-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            selectedFile: null,
            resData: null,
            resDataJson: null
        }
    },
    methods: {
        onFileSelected(event) {
            this.selectedFile = event.target.files[0]
            

            console.log(this.selectedFile)
            const reader = new FileReader();

            reader.onload = function(e) {
                let previewImage = document.getElementById('preview-image')
                previewImage.src = e.target.result;
            };

            reader.readAsDataURL(this.selectedFile);
            
        },
        onUpload() {
            console.log("Uploading to server...")
            
            const title_json = document.getElementById('res-data-json-title');
            title_json.textContent = "Uploading...";
            


            const fd = new FormData();
            fd.append('file', this.selectedFile)

            axios.post('http://localhost:8008/predict',fd)
             .then(res => {
                console.log("Uploaded!")
                console.log(res)
                this.resData = res;
                this.resDataJson = JSON.stringify(res.data);

                const title_json = document.getElementById('res-data-json-title');
                const paragraph = document.getElementById('res-data-json');
                const table_title = document.getElementById('extract-data')
                
                title_json.textContent = "Chuỗi JSON trả về" ;
                paragraph.textContent = this.resDataJson;
             })

            
        }
    }
}
</script>

<style>
    img {
        width: 450px;
        height: 800px;
        overflow: auto
    }

    .res-data-json {
        width: 200px;
        height: 200px;
        overflow: auto
    }
</style>