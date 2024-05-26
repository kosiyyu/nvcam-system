<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue';
import autosize from 'autosize';

let internalValue = ref('');
let textarea = ref(null);

const props = defineProps({
  modelValue: String
});

watch(() => props.modelValue, (newVal) => {
  internalValue.value = newVal || '';
});

watch(internalValue, () => {
  nextTick(() => {
    autosize.update(textarea.value!);
  });
});

onMounted(() => {
  nextTick(() => {
    autosize(textarea.value!);
  });
});

defineEmits(['update:modelValue']);

</script>

<template>
  <textarea v-model="internalValue" ref="textarea"></textarea>
</template>