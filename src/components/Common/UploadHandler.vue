<script lang="ts" setup>
import { computed, ref } from 'vue'

const props = defineProps<{
  modelValue: File | null
}>()
const emit = defineEmits<{
  (e: 'update:modelValue', file: File | null): void
}>()
const isDragging = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)
const modelValue = computed({
  get: () => props.modelValue,
  set: (file: File | null) => {
    emit('update:modelValue', file)
  },
})

const handleDrop = (event: DragEvent) => {
  const files = event.dataTransfer?.files
  if (files && files.length) {
    uploadFile(files[0])
  }
  isDragging.value = false
}

const handleDragOver = (event: DragEvent) => {
  event.preventDefault()
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleClick = () => {
  fileInput.value?.click()
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    uploadFile(target.files[0])
  }
}

const uploadFile = (file: File) => {
  console.log('上傳文件:', file)
  modelValue.value = file
}
</script>
<template>
  <div
    class="flex items-center justify-center flex-grow h-10 bg-slate-600 border-2 border-dashed border-slate-400 rounded-lg cursor-pointer transition-colors"
    :class="{
      'bg-slate-500 border-slate-300': isDragging,
      'bg-slate-600 border-slate-400': !isDragging,
    }"
    @drop.prevent="handleDrop"
    @dragover.prevent="handleDragOver"
    @dragleave="handleDragLeave"
    @click="handleClick"
  >
    <p class="px-2 text-center text-sm text-slate-200">
      {{ modelValue ? modelValue.name : '拖放檔案至此處 -或- 點擊上傳' }}
    </p>
    <input type="file" ref="fileInput" class="hidden" @change="handleFileChange" />
  </div>
</template>
