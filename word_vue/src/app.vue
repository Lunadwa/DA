<template>
  <div class="flex flex-col h-screen p-2">
    <el-upload
      ref="uploadRef"
      class="upload-demo"
      action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
      :auto-upload="false"
      :disabled="fileUploaded" 
      :file-list="fileList"
      :on-remove="handleRemove"
      @change = "handleFileChange"
    >
      <template #trigger>
        <el-button type="primary" class="add-margin" :disabled="fileList.length >= 1">选择文件</el-button>
      </template>
      
      <el-button
      v-loading.fullscreen.lock="fullscreenLoading"
      type="success"
      @click="getFileContent"
      >
      文件解析
    </el-button>
    
      <template #tip>
        <div class="el-upload__tip">
          只能上传word文件
        </div>
      </template>
    </el-upload>

    <component :is="component" :prasedDate="prasedDate" v-bind="$attrs"></component>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import VueComposition from './vue-composition'
import axios from 'axios';

const selectedFile = ref(null); // 保存文件对象
const formData = new FormData();

export default {
  components: {
    VueComposition,
  },
  data(){
    return {
      prasedDate: null,// 用于存储从后端返回的数据
      fullscreenLoading: false, // 控制全屏加载状态的变量
      fileUploaded: false, // 文件是否已上传的标志
      fileList: [], // 存储文件列表
    }
  },
  setup() {
    const type = ref('composition');
    const component = computed(
      () =>
        ({
          composition: VueComposition,
        }[type.value])
    );
    return {
      type,
      component,
    };
  },
  methods:{
    handleFileChange(file){
      console.log('选择的文件是:', file.name);
      selectedFile.value = file.raw
      // 设置文件已上传的标志为 true
      this.fileList = [file]; // 限制只保留最后选择的一个文件
      this.fileUploaded = true; // 标记文件已上传
    },

    handleRemove(file) {
      console.log('删除文件:', file.name);
      selectedFile.value = null; // 删除文件时将 selectedFile 设置为 null
      this.fileList = []; // 清空文件列表
      this.fileUploaded = false; // 标记文件未上传
    },

    async getFileContent(){
      if (!selectedFile.value) {
        return; // 如果没有选择文件，不执行后续操作
      }

      formData.append('file', selectedFile.value);
      this.fullscreenLoading = true; // 设置 fullscreenLoading 为 true，显示全屏加载状态

      try{
        const response = await axios.post('http://127.0.0.1:5000/get_all_contents', formData);
        this.prasedDate = response.data.content; // 将后端返回的数据赋值给 prasedDate
        console.log('响应数据类型：',typeof this.prasedDate)
      }catch (error) {
        console.error('获取文件内容失败:', error);
      }finally {
           this.fullscreenLoading = false; // 隐藏全屏加载状态
      }
    } 
  }
};
</script>

<style>
@import url('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.0/dist/tailwind.min.css');

h1,
p {
  font-family: Lato;
}
/* 添加间距的样式 */
.add-margin {
  margin-right: 10px; /* 添加 2px 的右边距 */
}
/* 禁用上传按钮时的样式 */
.el-upload__trigger.is-disabled {
  /* 样式设置为灰色 */
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
