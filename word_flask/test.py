<template>
  <div>
    <h1 class="upload-title" style="margin-top: 20px;">需求文档AI分析</h1>
    <div class="upload-container">
      <div class="center-container">
        <el-upload class="upload-demo" :auto-upload="false" :show-file-list="false" drag action=""  @change="handleFileChange">
          <div class="el-upload__text" v-if="selectedFileName">
            已选择文件: {{ selectedFileName }}
          </div>
          <div class="el-upload__text" v-else>
            将文件拖到此处，或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">只能上传 Word 文件</div>
          </template>
        </el-upload>
        <el-button class="parse-button" type="primary" @click="getFileContent">文件解析</el-button> <!-- 添加文件解析按钮 -->

        <div class="custom-content-container">
        <!-- 文件内容显示的区域 -->
          <div class="left-content">
            <!-- 将文件内容的代码移动到这里 -->
            <div class="file-content" :style="{ height: fileContentHeight + 'px' }">
              <pre class="file-text">{{ fileContent }}</pre>
            </div>
          </div>
           <!-- 蓝色竖线 -->
          <div class="blue-line"></div>

          <!-- 思维导图展示区域 -->
          <div class="right-content">
            <!-- 这里是思维导图展示区域 -->
            <svg id="markmapSvg" style="width: 100%; height: 600px;"></svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { Transformer } from 'markmap-lib';
import { Markmap } from 'markmap-view';
import { ElMessage } from 'element-plus';
import axios from 'axios';

export default {
  setup() {
    const selectedFile = ref(null); // 保存文件对象
    const selectedFileName = ref(''); // 保存文件名
    const fileContent = ref(''); // 文件内容
    const fileContentHeight = ref(0); // 文件内容区域的高度
    const isEditing = ref(false);
    const editedContent = ref('');

   const handleFileChange = async (file) => {
      if (file && file.raw) {
        const fileName = file.raw.name;
        console.log('选择的文件:', fileName);
        const isWord = fileName.substring(fileName.lastIndexOf('.') + 1); // 通过符号切割获取文件后缀
        const extension = isWord === 'doc';
        const extension1 = isWord === 'docx';
        if (!extension && !extension1) {
          ElMessage.error('只能上传 Word 文件');
          return false; // 阻止上传
        } else {
          selectedFile.value = file.raw; // 保存文件对象
          selectedFileName.value = fileName; // 保存文件名
          return true; // 允许上传
        }
      }
    };

  const toggleEditMode = () => {
      isEditing.value = !isEditing.value;
      if (isEditing.value) {
        editedContent.value = fileContent.value;
      }
    };

    const saveAndToggleEditMode = () => {
      fileContent.value = editedContent.value;
      isEditing.value = false;
    };

 const getFileContent = async () => {
      if (!selectedFileName.value) {
        console.error('未选择文件');
        return;
      }

      const formData = new FormData();
      formData.append('file', selectedFile.value);
      console.log(selectedFile.value)
      try {
        const response = await axios.post('http://127.0.0.1:5000/get_all_contents', formData);
        console.log('后端返回的文件内容:', response.data);

        // 将文件内容存储到响应式数据中
        fileContent.value = response.data.content;
        console.log('响应式数据内容:', response.data.content);

        try {
          // 使用 Transformer 函数将 Markdown 转换为 Markmap 所需的数据格式
          const transformer = new Transformer();
          const transformed = transformer.transform(fileContent.value);
          console.log('转换后的数据:', transformed);

          // 获取 SVG 容器
          const svgContainer = document.querySelector('#markmapSvg');
          if (!svgContainer) {
            console.error('找不到 SVG 容器');
            return;
          }

          try {
            // 渲染 Markmap 到 SVG 容器
            Markmap.create(svgContainer, undefined, transformed);
          } catch (error) {
            console.error('渲染 Markmap 实例时出错:', error);
          }

          // 获取内容高度并动态调整展示区域的高度
          const contentArea = document.querySelector('.file-content');
          if (contentArea) {
            fileContentHeight.value = contentArea.scrollHeight;
          }
        } catch (error) {
          console.error('加载数据失败:', error);
        }

        // 获取内容高度并动态调整展示区域的高度
        const contentArea = document.querySelector('.file-content');
        if (contentArea) {
          fileContentHeight.value = contentArea.scrollHeight;
        }
      } catch (error) {
        console.error('获取文件内容失败:', error);
      }
    };

    return {
      selectedFileName,
      fileContent,
      handleFileChange,
      getFileContent,
      isEditing,
      editedContent,
      toggleEditMode,
      saveAndToggleEditMode
    };
  }
};
</script>

<style scoped>
.custom-content-container {
  width: 1600px;
  height: 800px;
  border: 1px solid lightblue; /* 容器边框颜色 */
  display: flex;
  margin: 20px auto 0; /* 上传文件按钮与容器间距，以及居中展示 */
  justify-content: center; /* 横向内容居中 */
  align-items: flex-start; /* 或者注释掉这行样式 */
  padding: 20px; /* 内边距 */
  box-sizing: border-box;
  position: relative; /* 相对定位 */
}
/* 蓝色竖线样式 */
.blue-line {
  position: absolute; /* 绝对定位 */
  width: 2px; /* 竖线宽度 */
  height: 100%; /* 容器高度 */
  background-color: lightblue; /* 蓝色 */
  left: 50%; /* 位于容器中间 */
  transform: translateX(-50%); /* 居中 */
}
/* 左侧区域样式 */
.left-content {
  width: calc(50% - 1px); /* 左侧宽度为容器的一半减去1px用于分隔线 */
  height: 100%;
  border-right: 1px solid lightblue; /* 右侧添加分隔线 */
  padding: 20px;
  box-sizing: border-box;
}
/* 右侧区域样式 */
.right-content {
  width: calc(50% - 1px);
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
}
/* 文件内容文本样式 */
.file-text {
  font-size: 18px; /* 字体大小 */
  white-space: pre-wrap; /* 换行 */
  text-align: left; /* 文本居左对齐 */
}
/* 文件内容区域样式 */
.file-content {
  overflow-y: auto; /* 垂直滚动条 */
}
</style>
