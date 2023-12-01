<template>
    <el-input
      v-model="inputValue"
      :rows="15"
      type="textarea"
      placeholder="此区域为AI生成需求文档Markdown格式数据区域，可以对此操作！"/>
  <svg class="flex-1" ref="svgRef" />
</template>

<script>
import { ref, watch, onMounted, onUpdated} from 'vue';
import { Transformer } from 'markmap-lib';
import { Markmap } from 'markmap-view';

const transformer = new Transformer();

export default {
  props: {
    prasedDate: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const svgRef = ref();
    const inputValue = ref(props.prasedDate);
    let mm;

    // 当 prasedDate 改变时，更新 inputValue 的值
    watch(() => props.prasedDate, (newValue) => {
      inputValue.value = newValue;
      update();
    });

    const update = () => {
      if (inputValue.value) { // 添加检查以确保 inputValue 有有效值
        const {root} = transformer.transform(inputValue.value);
        mm.setData(root);
        mm.fit();
      }
    };

    const updateMap = () => {
      update();
    };

    onMounted(()=> {
      mm = Markmap.create(svgRef.value)
      update();
    });

    onUpdated(update)

    return {
      svgRef,
      inputValue,
      updateMap,
    };
  }
};
</script>
