<template>
  <div class="flex flex-grow bg-slate-800 gap-2 p-2">
    <div class="flex flex-col w-full max-w-2xl mx-auto">
      <div
        class="flex flex-col w-full text-lg text-slate-100 bg-slate-700 rounded-lg shadow-lg border border-slate-600"
      >
        <div class="flex items-center">
          <div
            class="px-3 py-1 text-sm text-slate-100 bg-slate-600 rounded shadow-lg border border-slate-500"
          >
            Single Audio Generate
          </div>
        </div>
        <div class="p-3 space-y-4">
          <div class="flex flex-col gap-2">
            <label class="text-sm text-slate-200">Enter text to generate:</label>
            <textarea
              v-model="singleText"
              rows="4"
              placeholder="Enter the text you want to convert to speech..."
              class="p-3 text-sm text-slate-900 bg-slate-100 rounded focus:border-orange-500 border border-slate-300 resize-vertical"
            ></textarea>
          </div>

          <div class="flex flex-col gap-2">
            <label class="text-sm text-slate-200">Select Speaker:</label>
            <select
              v-model="selectedSpeaker"
              class="p-2 text-sm text-slate-900 bg-slate-100 rounded focus:border-orange-500 border border-slate-300"
            >
              <option value="">Choose a speaker...</option>
              <option value="speaker1">Speaker 1</option>
              <option value="speaker2">Speaker 2</option>
              <option value="speaker3">Speaker 3</option>
            </select>
          </div>

          <div class="flex items-center gap-2">
            <label class="text-sm text-slate-200">Quality Check:</label>
            <input
              v-model="singleQualityCheck"
              type="checkbox"
              class="form-checkbox accent-blue-500"
            />
            <span class="text-xs text-slate-400">(*Check audio quality but may increase time)</span>
          </div>

          <div class="flex items-center justify-center">
            <button
              class="py-2 px-6 text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
              @click="handleSingleGenerateClick"
            >
              Generate Audio
            </button>
          </div>

          <div class="min-h-[32px] px-3 py-2 text-sm text-slate-200 bg-slate-600 rounded">
            {{ singleGenerateResult }}
          </div>

          <!-- 顯示生成的音訊 -->
          <div v-if="audioUrl" class="flex flex-col gap-2">
            <label class="text-sm text-slate-200">Generated Audio:</label>
            <audio controls class="w-full">
              <source :src="audioUrl" type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>
            <div class="flex justify-center">
              <a
                :href="audioUrl"
                download="generated_audio.mp3"
                class="py-2 px-4 text-sm text-white bg-green-500 rounded hover:bg-green-600 cursor-pointer transition-colors"
              >
                Download Audio
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import axios from 'axios'

// Single Generate 頁面專用的狀態
const singleText = ref('')
const selectedSpeaker = ref('')
const singleQualityCheck = ref(false)
const singleGenerateResult = ref('Ready to generate...')
const audioUrl = ref('')

// Single Generate 功能函數
const handleSingleGenerateClick = async () => {
  singleGenerateResult.value = 'Now generating...please wait'
  audioUrl.value = ''

  if (!singleText.value.trim()) {
    singleGenerateResult.value = 'Please enter text to generate'
    return
  }

  if (!selectedSpeaker.value) {
    singleGenerateResult.value = 'Please select a speaker'
    return
  }

  try {
    // 這裡是示例API調用，你需要根據實際的API來修改
    const url = `http://52.183.25.173:52010/single_generate`
    const formData = new FormData()
    formData.append('text', singleText.value)
    formData.append('speaker', selectedSpeaker.value)
    formData.append('quality_check', singleQualityCheck.value.toString())

    const response = await axios.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 30000, // 30秒超時，因為音訊生成可能需要較長時間
    })

    const contentType = response.headers['content-type']
    if (contentType && contentType.indexOf('application/json') !== -1) {
      // Handle JSON response (error message)
      const json = response.data
      if (json.status === 'FAILED') {
        singleGenerateResult.value = json.message
      } else if (json.status === 'OK') {
        singleGenerateResult.value = 'Audio generated successfully!'
        // 如果API返回音訊URL
        if (json.audio_url) {
          audioUrl.value = json.audio_url
        }
      } else {
        singleGenerateResult.value = 'Unexpected response format'
      }
    } else {
      // Handle Blob response (audio file)
      const blob = new Blob([response.data], { type: 'audio/mpeg' })
      audioUrl.value = window.URL.createObjectURL(blob)
      singleGenerateResult.value = 'Audio generated successfully!'
    }
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
      singleGenerateResult.value = 'The request timed out. Please try again.'
    } else {
      singleGenerateResult.value = 'An error occurred. Please try again.'
    }
    console.error(error)
  }
}
</script>
