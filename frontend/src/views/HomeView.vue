<template>
 <div>
    <div class="intro">
      <h1>OCR-Free Document Parsing</h1>
      <p>Chúng tôi triển khai module trích xuất thông tin từ hình ảnh hóa đơn sử dụng mô hình Donut - viết tắt của Document Understanding Transformer</p>
      <p>Khác với các phương pháp trước đó sử dụng kết quả của OCR cho tác vụ parsing, mô hình này là một phương pháp đọc hiểu tài liệu end-to-end</p>
      <p>Donut đạt hiệu suất tốt cả về mặt độ chính xác lẫn tốc độ thực thi do phụ thuộc vào tác vụ OCR.</p>
    </div>

   

    <a-button type="primary" :size="large">
      <router-link :to="{name: 'inference'}">
        Bắt đầu ngay!
      </router-link>
    </a-button>
  <router-view/>
 </div>
</template>

<script>

export default {
  name: 'HomeView',
  components: {
    
  }
}
</script>

<style>
 
</style>
