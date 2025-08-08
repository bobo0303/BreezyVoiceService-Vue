<script lang="ts" setup>
import { ref, provide } from 'vue'
import axios from 'axios'
import TaskGenerateView from '@/views/TaskGenerateView.vue'
import SingleGenerateView from '@/views/SingleGenerateView.vue'
import WalkerCompose from '@/views/WalkerCompose.vue'

// 共用狀態
const taskId = ref('')
const speakerUploadFile = ref<File | null>(null)
const txtUploadFile = ref<File | null>(null)
const csvUploadFile = ref<File | null>(null)
const stateResult = ref('')
const speakerUploadResult = ref('')
const csvUploadResult = ref('')
const speakerList = ref<string | string[]>('')
const logList = ref<string | string[]>('')
const isPageSwitcherVisible = ref(false)
const currentPage = ref('task-generate')
const expansionRatio = ref(1)
const downloadUrl = ref('')
const downloadaudios = ref('')
const qualityCheck = ref(false)
const threadRatio = ref(1)
const threadSuggestion = ref('')
const generateResult = ref('')
const optResult = ref('')
const csvCheckResult = ref('')
const isTooltipVisible = ref(false)
const isTxtTipVisible = ref(false)
const isCatTipVisible = ref(false)
const isGenerateTipVisible = ref(false)
const tooltipX = ref(0)
const tooltipY = ref(0)

// 提供給子組件使用
provide('taskId', taskId)
provide('speakerUploadFile', speakerUploadFile)
provide('txtUploadFile', txtUploadFile)
provide('csvUploadFile', csvUploadFile)
provide('stateResult', stateResult)
provide('speakerUploadResult', speakerUploadResult)
provide('csvUploadResult', csvUploadResult)
provide('speakerList', speakerList)
provide('logList', logList)
provide('expansionRatio', expansionRatio)
provide('downloadUrl', downloadUrl)
provide('downloadaudios', downloadaudios)
provide('qualityCheck', qualityCheck)
provide('threadRatio', threadRatio)
provide('threadSuggestion', threadSuggestion)
provide('generateResult', generateResult)
provide('optResult', optResult)
provide('csvCheckResult', csvCheckResult)
provide('isTooltipVisible', isTooltipVisible)
provide('isTxtTipVisible', isTxtTipVisible)
provide('isGenerateTipVisible', isGenerateTipVisible)
provide('tooltipX', tooltipX)
provide('tooltipY', tooltipY)

// 工具函數
const showToolTip = () => {
  isTooltipVisible.value = true
}

const hideToolTip = () => {
  isTooltipVisible.value = false
}

const showCatTip = () => {
  isCatTipVisible.value = true
}

const hideCatTip = () => {
  isCatTipVisible.value = false
}

const showTxtTip = () => {
  isTxtTipVisible.value = true
}

const hideTxtTip = () => {
  isTxtTipVisible.value = false
}

const showGenerateTip = () => {
  isGenerateTipVisible.value = true
}

const hideGenerateTip = () => {
  isGenerateTipVisible.value = false
}

const updateTooltipPosition = (event: MouseEvent) => {
  tooltipX.value = event.pageX + 10
  tooltipY.value = event.pageY + 10
}

const updateTxtTipPosition = (event: MouseEvent) => {
  tooltipX.value = event.pageX - 300
  tooltipY.value = event.pageY + 10
}

const updateGenerateTipPosition = (event: MouseEvent) => {
  tooltipX.value = event.pageX - 500
  tooltipY.value = event.pageY + 10
}

const togglePageSwitcher = () => {
  isPageSwitcherVisible.value = !isPageSwitcherVisible.value
}

const closePageSwitcher = () => {
  isPageSwitcherVisible.value = false
}

const switchToPage = (pageName: string) => {
  currentPage.value = pageName
  closePageSwitcher()
}

const handleStateButtonClick = async () => {
  stateResult.value = 'Now processing...please wait'
  const url = `http://52.183.25.173:52010/task_status?task_id=${taskId.value}`
  if (!taskId.value) {
    stateResult.value = 'Please enter a Task ID'
    return
  }
  try {
    const response = await axios.get(url, {
      timeout: 10000,
    })
    if (response.data['status'] === 'FAILED') {
      stateResult.value = response.data['message']
      return
    } else if (response.data['status'] === 'OK') {
      stateResult.value = ` | State: ${response.data['data']['state']} | Progress: ${response.data['data']['progress']} \
                    | Total audio: ${response.data['data']['audio_count']} | Keep: ${response.data['data']['keep']} \
                    | Delete: ${response.data['data']['del']} | Unprocessed: ${response.data['data']['unprocessed']} | `
    } else {
      stateResult.value = response.data
    }
    console.log(response.data)
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
      stateResult.value = 'The request timed out. Please try again.'
    } else {
      stateResult.value = 'An error occurred. Please try again.'
    }
    console.error(error)
  }
}

const handleSpeakerUploadClick = async () => {
  speakerUploadResult.value = 'Now processing...please wait'
  const url = `http://52.183.25.173:52010/custom_speaker_upload?task_id=${taskId.value}`
  if (!speakerUploadFile.value) {
    speakerUploadResult.value = 'Please select a file to upload'
    return
  }
  if (!speakerUploadFile.value.name.endsWith('.zip')) {
    speakerUploadResult.value = 'Only .zip files are allowed'
    return
  }
  if (!taskId.value) {
    speakerUploadResult.value = 'Please enter a Task ID'
    return
  }
  const formData = new FormData()
  formData.append('file', speakerUploadFile.value)
  try {
    const response = await axios.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 10000,
    })
    if (response.data['status'] === 'FAILED' || response.data['status'] === 'OK') {
      speakerUploadResult.value = response.data['message']
    } else {
      speakerUploadResult.value = response.data
    }
    console.log(response.data)
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
      speakerUploadResult.value = 'The request timed out. Please try again.'
    } else {
      speakerUploadResult.value = 'An error occurred. Please try again.'
    }
    console.error(error)
  }
}

const handleSpeakerListClick = async () => {
  speakerList.value = 'Now processing...please wait'
  const url = `http://52.183.25.173:52010/speaker_list?task_id=${taskId.value}`
  if (!taskId.value) {
    speakerList.value = 'Please enter a Task ID'
    return
  }
  try {
    const response = await axios.get(url, {
      timeout: 10000,
    })
    if (response.data['status'] === 'FAILED') {
      speakerList.value = response.data['message']
      return
    } else if (response.data['status'] === 'OK') {
      speakerList.value = response.data['data']
    } else {
      speakerList.value = response.data
    }
    console.log(response.data)
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
      speakerList.value = 'The request timed out. Please try again.'
    } else {
      speakerList.value = 'An error occurred. Please try again.'
    }
    console.error(error)
  }
}

const handleCSVClick = async () => {
  csvUploadResult.value = 'Now processing...please wait'
  downloadUrl.value = ''
  const url = `http://52.183.25.173:52010/txt2csv?task_id=${taskId.value}&expansion_ratio=${expansionRatio.value}`
  if (!txtUploadFile.value) {
    csvUploadResult.value = 'Please select a file to upload'
    return
  }
  if (!txtUploadFile.value.name.endsWith('.txt')) {
    csvUploadResult.value = 'Only .txt files are allowed'
    return
  }
  if (!taskId.value) {
    csvUploadResult.value = 'Please enter a Task ID'
    return
  }
  const formData = new FormData()
  formData.append('file', txtUploadFile.value)
  try {
    const response = await axios.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob', // 添加這個來正確處理二進制數據
      timeout: 10000,
    })
    const contentType = response.headers['content-type']

    // 檢查是否為錯誤響應（通常是 JSON 格式）
    if (contentType && contentType.indexOf('application/json') !== -1) {
      // 將 blob 轉換為文本來讀取錯誤消息
      const text = await response.data.text()
      const json = JSON.parse(text)
      if (json.status === 'FAILED') {
        csvUploadResult.value = json.message
      } else {
        csvUploadResult.value = 'Unexpected response format'
      }
    } else if (contentType && contentType.indexOf('text/plain') !== -1) {
      // 將 blob 轉換為文本來讀取錯誤消息
      const text = await response.data.text()
      csvUploadResult.value = text
    } else {
      // 處理 CSV 文件 - 添加 UTF-8 BOM 來確保中文正確顯示
      const BOM = '\uFEFF' // UTF-8 BOM
      const csvText = await response.data.text()
      const blob = new Blob([BOM + csvText], { type: 'text/csv;charset=utf-8' })
      downloadUrl.value = window.URL.createObjectURL(blob)
      csvUploadResult.value = 'CSV file generated successfully'
    }
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
      csvUploadResult.value = 'The request timed out. Please try again.'
    } else {
      csvUploadResult.value = 'An error occurred. Please try again.'
    }
    console.error(error)
  }
}

const handleThreadSuggestionClick = async () => {
  threadSuggestion.value = 'Now processing...please wait'
  const url = `http://52.183.25.173:52010/thread_suggestion`
  try {
    const response = await axios.get(url, {
      timeout: 10000,
    })
    if (response.data['status'] === 'FAILED') {
      threadSuggestion.value = response.data['message']
      return
    } else if (response.data['status'] === 'OK') {
      threadSuggestion.value = ` | Thread Suggestion: ${response.data['data']} | `
    } else {
      threadSuggestion.value = response.data
    }
    console.log(response.data)
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
      threadSuggestion.value = 'The request timed out. Please try again.'
    } else {
      threadSuggestion.value = 'An error occurred. Please try again.'
    }
    console.error(error)
  }
}

const handleCheckCsvClick = async () => {
  csvCheckResult.value = 'Now processing...please wait (if file is large, it may take a while)'
  downloadUrl.value = ''
  const url = `http://52.183.25.173:52010/check_csv_format`
  if (!csvUploadFile.value) {
    csvCheckResult.value = 'Please select a file to upload'
    return
  }
  if (!csvUploadFile.value.name.endsWith('.csv')) {
    csvCheckResult.value = 'Only .csv files are allowed'
    return
  }

  const formData = new FormData()
  formData.append('csv_file', csvUploadFile.value)
  try {
    const response = await axios.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    if (response.data['status'] === 'FAILED') {
      csvCheckResult.value = response.data['message']
      return
    } else if (response.data['status'] === 'OK') {
      csvCheckResult.value = response.data['message']
    } else {
      csvCheckResult.value = response.data
    }
    console.log(response.data)
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
      csvCheckResult.value = 'The request timed out. Please try again.'
    } else {
      csvCheckResult.value = 'An error occurred. Please try again.'
    }
    console.error(error)
  }
  console.log(csvCheckResult.value)
}

const handlestartgenerateClick = async () => {
  generateResult.value = 'Now processing...please wait'
  const url = `http://52.183.25.173:52010/batch_generate`

  if (!csvUploadFile.value) {
    generateResult.value = 'Please select a file to upload'
    return
  }

  if (!csvUploadFile.value.name.endsWith('.csv')) {
    generateResult.value = 'Only .csv files are allowed'
    return
  }

  if (!taskId.value) {
    generateResult.value = 'Please enter a Task ID'
    return
  }

  const formData = new FormData()
  formData.append('csv_file', csvUploadFile.value!)
  formData.append('task_id', taskId.value)
  formData.append('quality_check', qualityCheck.value.toString())
  formData.append('num_thread', threadRatio.value.toString())
  console.log(
    `Task ID: ${taskId.value}, Quality Check: ${qualityCheck.value}, Thread Ratio: ${threadRatio.value}`,
  )
  try {
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()

    if (data.status === 'FAILED') {
      generateResult.value = data.message
      return
    } else if (data.status === 'OK') {
      generateResult.value = ` | Generation has begun. You can check state by [Check state] | `
    } else {
      generateResult.value = data
    }

    console.log(data)
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error)
    generateResult.value = 'Error processing the request'
  }
}

const handleCheckLogClick = async () => {
  logList.value = 'Now processing...please wait'
  const url = `http://52.183.25.173:52010/show_logs`
  try {
    const response = await axios.get(url, {
      timeout: 10000,
    })
    if (response.data['status'] === 'FAILED') {
      logList.value = response.data['message']
      return
    } else if (response.data['status'] === 'OK') {
      logList.value = response.data['data']
    } else {
      logList.value = response.data
    }
    console.log(response.data)
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
      logList.value = 'The request timed out. Please try again.'
    } else {
      logList.value = 'An error occurred. Please try again.'
    }
    console.error(error)
  }
}

const handlecancelClick = async () => {
  downloadaudios.value = ''
  optResult.value = 'Try to stop task ... please wait'
  const url = `http://52.183.25.173:52010/cancel_task?task_id=${taskId.value}`
  if (!taskId.value) {
    optResult.value = 'Please enter a Task ID'
    return
  }
  try {
    const response = await axios.post(url, {})
    if (response.data['status'] === 'FAILED') {
      optResult.value = response.data['message']
      return
    } else if (response.data['status'] === 'OK') {
      optResult.value = response.data['message']
    } else {
      optResult.value = response.data
    }
    console.log(response.data)
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
      optResult.value = 'The request timed out. Please try again.'
    } else {
      optResult.value = 'An error occurred. Please try again.'
    }
    console.error(error)
  }
}

const handleDeleteClick = async () => {
  downloadaudios.value = ''
  optResult.value = 'Try to delete task ... please wait'
  const url = `http://52.183.25.173:52010/delete_task?task_id=${taskId.value}`
  if (!taskId.value) {
    optResult.value = 'Please enter a Task ID'
    return
  }
  try {
    const response = await axios.delete(url, {})
    if (response.data['status'] === 'FAILED') {
      optResult.value = response.data['message']
      return
    } else if (response.data['status'] === 'OK') {
      optResult.value = response.data['message']
    } else {
      optResult.value = response.data
    }
    console.log(response.data)
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
      optResult.value = 'The request timed out. Please try again.'
    } else {
      optResult.value = 'An error occurred. Please try again.'
    }
    console.error(error)
  }
}

const handleGetAudiosClick = async () => {
  downloadaudios.value = ''
  optResult.value = 'Try to get audios ... please wait'
  const url = `http://52.183.25.173:52010/get_audio?task_id=${taskId.value}`
  if (!taskId.value) {
    optResult.value = 'Please enter a Task ID'
    return
  }
  try {
    const response = await axios.get(url, {
      responseType: 'blob', // 關鍵修改：指定響應類型為 blob
    })
    const contentType = response.headers['content-type']

    // 檢查是否為錯誤響應（通常是 JSON 格式）
    if (contentType && contentType.indexOf('application/json') !== -1) {
      // 將 blob 轉換為文本來讀取錯誤消息
      const text = await response.data.text()
      const json = JSON.parse(text)
      if (json.status === 'FAILED') {
        optResult.value = json.message
      } else {
        optResult.value = 'Unexpected response format'
      }
    } else if (contentType && contentType.indexOf('text/plain') !== -1) {
      // 將 blob 轉換為文本來讀取錯誤消息
      const text = await response.data.text()
      optResult.value = text
    } else {
      // 處理二進制響應（ZIP 文件）
      const blob = new Blob([response.data], { type: 'application/zip' }) // 修改為正確的 ZIP MIME 類型
      downloadaudios.value = window.URL.createObjectURL(blob)
      optResult.value = 'Task "' + taskId.value + '" Download audios ready'
    }
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
      optResult.value = 'The request timed out. Please try again.'
    } else {
      optResult.value = 'An error occurred. Please try again.'
    }
    console.error(error)
  }
}

// 提供所有函數給子組件
provide('showToolTip', showToolTip)
provide('hideToolTip', hideToolTip)
provide('showCatTip', showCatTip)
provide('hideCatTip', hideCatTip)
provide('showTxtTip', showTxtTip)
provide('hideTxtTip', hideTxtTip)
provide('showGenerateTip', showGenerateTip)
provide('hideGenerateTip', hideGenerateTip)
provide('updateTooltipPosition', updateTooltipPosition)
provide('updateTxtTipPosition', updateTxtTipPosition)
provide('updateGenerateTipPosition', updateGenerateTipPosition)
provide('handleSpeakerUploadClick', handleSpeakerUploadClick)
provide('handleSpeakerListClick', handleSpeakerListClick)
provide('handleCSVClick', handleCSVClick)
provide('handleThreadSuggestionClick', handleThreadSuggestionClick)
provide('handleCheckCsvClick', handleCheckCsvClick)
provide('handlestartgenerateClick', handlestartgenerateClick)
provide('handleCheckLogClick', handleCheckLogClick)
provide('handlecancelClick', handlecancelClick)
provide('handleDeleteClick', handleDeleteClick)
provide('handleGetAudiosClick', handleGetAudiosClick)
</script>

<template>
  <div class="relative min-h-screen flex flex-col">
    <button
      class="fixed top-[0.5vw] left-[0.5vw] z-50 p-2 bg-slate-700 text-slate-100 rounded hover:bg-slate-600 cursor-pointer transition-colors border border-slate-600"
      @click="togglePageSwitcher"
    >
      ☰
    </button>
    <div
      v-if="isPageSwitcherVisible"
      class="fixed inset-0 z-40 bg-black bg-opacity-50"
      @click="closePageSwitcher"
    ></div>
    <div
      v-if="isPageSwitcherVisible"
      class="fixed top-[4vw] left-[2vw] z-50 w-64 bg-slate-700 rounded-lg shadow-lg border border-slate-600"
    >
      <ul>
        <li>
          <button
            class="flex items-center w-full px-1 py-2 text-left text-slate-200 rounded hover:bg-slate-600 hover:text-slate-100 transition-colors"
            :class="{ 'bg-slate-600': currentPage === 'task-generate' }"
            @click="switchToPage('task-generate')"
          >
            <img src="D:\bobo\bv_vue\src\assets\B.png" alt="Icon 1" class="w-6 h-6 mx-1 mr-2" />
            task generate
          </button>
        </li>
        <!-- <li>
          <button
            class="flex items-center w-full px-1 py-2 text-left text-slate-200 rounded hover:bg-slate-600 hover:text-slate-100 transition-colors"
          >
            <img src="D:\bobo\bv_vue\src\assets\BB.png" alt="Icon 2" class="w-6 h-6 mx-1 mr-2" />
            model test
          </button>
        </li> -->
        <li>
          <button
            class="flex items-center w-full px-1 py-2 text-left text-slate-200 rounded hover:bg-slate-600 hover:text-slate-100 transition-colors"
            :class="{ 'bg-slate-600': currentPage === 'single-generate' }"
            @click="switchToPage('single-generate')"
          >
            <img src="D:\bobo\bv_vue\src\assets\BBB.png" alt="Icon 3" class="w-6 h-6 mx-1 mr-2" />
            Single generate
          </button>
        </li>
      </ul>
    </div>

    <div
      class="flex justify-between items-center ml-2 px-10 py-3 text-xl text-slate-100 bg-gradient-to-r from-slate-800 to-slate-700"
    >
      <div
        class="flex flex-row"
        @mouseover="showCatTip"
        @mouseleave="hideCatTip"
        @mousemove="updateTooltipPosition"
      >
        BreezeVoice Audio Generate /ᐠ .ᆺ. ᐟ\ﾉ
        <div v-if="isCatTipVisible">
          <img src="@/assets/cat.gif" alt="Example GIF" class="w-6 h-6 ml-5 mt-1" />
        </div>
      </div>

      <textarea
        rows="1"
        v-model="taskId"
        class="p-1 text-sm text-slate-900 bg-slate-100 rounded focus:border-orange-500 border border-slate-300"
        placeholder="Enter Task ID"
      ></textarea>
    </div>

    <!-- Task Generate 頁面 -->
    <TaskGenerateView v-if="currentPage === 'task-generate'" />

    <!-- Single Generate 頁面 -->
    <SingleGenerateView v-if="currentPage === 'single-generate'" />

    <!-- Check State 區域 (兩個頁面共用) -->
    <div
      class="flex items-center gap-2 w-[calc(100% - 1rem)] p-3 ml-2 mr-2 mb-2 text-slate-100 bg-slate-700 rounded-lg shadow-lg border border-slate-600"
    >
      <button
        class="py-2 px-3 text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
        @click="handleStateButtonClick"
      >
        Check State
      </button>
      <div class="flex-grow min-h-[32px] px-3 py-2 text-sm text-slate-200 bg-slate-600 rounded">
        {{ stateResult }}
      </div>
    </div>
    <div>
      <WalkerCompose />
    </div>
  </div>
</template>

<style scoped>
/* 定义渐淡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>
