<template>
  <div class="flex flex-grow bg-slate-800 gap-2 p-2">
    <div class="hidden md:flex flex-col w-1/3">
      <div
        class="flex flex-col w-full text-lg text-slate-100 bg-slate-700 rounded-lg shadow-lg border border-slate-600"
      >
        <div class="flex items-center justify-between">
          <div
            class="px-3 py-1 text-sm text-slate-100 bg-slate-600 rounded shadow-lg border border-slate-500"
          >
            Custom Speakers upload
          </div>
          <img
            src="@/assets/samples/exclamation.png"
            alt="Icon"
            class="hidden lg:block w-4 h-4 mt-3 mr-3 cursor-pointer"
            @mouseover="showToolTip"
            @mouseleave="hideToolTip"
            @mousemove="updateTooltipPosition"
          />
          <transition name="fade">
            <div
              v-if="isTooltipVisible"
              :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }"
              class="fixed z-50 p-2 text-slate-100 bg-slate-700 rounded shadow-lg border border-slate-600"
            >
              <img src="@/assets/samples/speaker_sample.png" alt="Tooltip Image" />
            </div>
          </transition>
        </div>
        <div class="p-3 space-y-2">
          <div class="flex items-center gap-2">
            <button
              class="px-3 py-2 whitespace-nowrap text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
              @click="handleSpeakerUploadClick"
            >
              Upload Speakers
            </button>
            <UploadHandler v-model="speakerUploadFile" />
          </div>
          <div class="min-h-[32px] p-3 text-sm text-slate-200 bg-slate-600 rounded">
            {{ speakerUploadResult }}
          </div>
        </div>
      </div>
      <div
        class="flex flex-col flex-grow w-full mt-3 text-lg text-slate-100 bg-slate-700 rounded-lg shadow-lg border border-slate-600"
      >
        <div class="flex items-start justify-between">
          <div
            class="px-3 py-1 text-sm text-slate-100 bg-slate-600 rounded shadow-lg border border-slate-500"
          >
            Speakers list
          </div>
          <button
            class="px-3 py-1 mt-3 mr-3 text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
            @click="handleSpeakerListClick"
          >
            List Speakers
          </button>
        </div>

        <div class="flex-grow h-[150px] m-3 bg-slate-600 rounded">
          <div class="h-full overflow-auto rounded">
            <template v-if="!taskId.trim()">
              <div class="p-3 text-sm text-slate-200 bg-slate-600 rounded text-center">
                Please enter Task ID to load speaker list
              </div>
            </template>
            <template v-else-if="Array.isArray(speakerList)">
              <ul class="p-2 text-sm bg-slate-600 rounded">
                <li
                  v-for="(speaker, index) in speakerList"
                  :key="speaker"
                  class="flex items-center text-slate-200 py-1 hover:bg-slate-500 cursor-pointer"
                  @click="selectSpeaker(speaker)"
                >
                  <input
                    type="radio"
                    :checked="selectedSpeaker === speaker"
                    :value="speaker"
                    name="speaker"
                    class="mr-2"
                    @change="selectSpeaker(speaker)"
                  />
                  <span class="flex-none w-8 text-center">{{ index + 1 }}.</span>
                  <span class="flex-grow">{{ speaker }}</span>
                </li>
              </ul>
            </template>
            <template v-else>
              <div class="p-3 text-sm text-slate-200 bg-slate-600 rounded">
                {{ speakerList }}
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>

    <div class="hidden md:flex flex-col w-1/3">
      <div
        class="flex flex-col w-full text-lg text-slate-100 bg-slate-700 rounded-lg shadow-lg border border-slate-600"
      >
        <div class="flex items-center justify-between">
          <div
            class="px-3 py-1 text-sm text-slate-100 bg-slate-600 rounded shadow-lg border border-slate-500"
          >
            Speaker audition
          </div>
        </div>
        <div class="flex-grow p-3">
          <template v-if="!selectedSpeaker">
            <div class="text-center text-slate-400 mt-6 mb-7">
              Please select a speaker from the left panel
            </div>
          </template>
          <template v-else>
            <div class="text-sm text-slate-200 mb-2 text-center">
              Selected speaker: {{ selectedSpeaker }}
            </div>

            <!-- Show loading message when no auditionAudioUrl -->
            <div v-if="!auditionAudioUrl" class="text-center text-slate-400 mt-5 mb-3">
              Loading speaker audio...
            </div>

            <!-- Show error message when auditionAudioUrl is text -->
            <div
              v-else-if="
                typeof auditionAudioUrl === 'string' && !auditionAudioUrl.startsWith('blob:')
              "
              class="text-center text-slate-400 mt-2"
            >
              {{ auditionAudioUrl }}
            </div>

            <!-- Show audio player when auditionAudioUrl is audio URL -->
            <div v-else-if="auditionAudioUrl.startsWith('blob:')" class="flex justify-center mt-2">
              <audio controls class="w-full max-w-sm" :src="auditionAudioUrl">
                Your browser does not support the audio element.
              </audio>
            </div>
          </template>
        </div>
      </div>
      <div
        class="flex flex-col h-1/3 w-full mt-3 text-lg text-slate-100 bg-slate-700 rounded-lg shadow-lg border border-slate-600"
      >
        <div class="flex items-center justify-between">
          <div
            class="px-3 py-1 text-sm text-slate-100 bg-slate-600 rounded shadow-lg border border-slate-500"
          >
            Generate text
          </div>
          <img
            src="@/assets/samples/exclamation.png"
            alt="Icon"
            class="hidden lg:block w-4 h-4 mt-3 mr-3 cursor-pointer"
            @mouseover="showGenerateTip"
            @mouseleave="hideGenerateTip"
            @mousemove="updateGenerateTipPosition"
          />
          <transition name="fade">
            <div
              v-if="isGenerateTipVisible"
              :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }"
              class="fixed z-50 p-2 text-slate-100 bg-slate-700 rounded shadow-lg border border-slate-600"
            >
              <img src="@/assets/samples/generate_sample.png" alt="Tooltip Image" />
            </div>
          </transition>
        </div>

        <div class="flex-grow p-3">
          <textarea
            v-model="singleText"
            placeholder="Enter text to generate speech..."
            class="w-full h-full p-2 text-sm text-slate-900 bg-slate-200 rounded border resize-none"
          ></textarea>
        </div>
      </div>
      <div
        class="flex flex-col flex-grow w-full mt-3 text-lg text-slate-100 bg-slate-700 rounded-lg shadow-lg border border-slate-600"
      >
        <div class="flex items-center">
          <div
            class="px-3 py-1 text-sm text-slate-100 bg-slate-600 rounded shadow-lg border border-slate-500"
          >
            Custom audio generation
          </div>
        </div>
        <div class="flex-grow p-3 space-y-3">
          <!-- 按鈕區域 - 水平置中排序 -->
          <div class="flex justify-between gap-3">
            <button
              class="px-3 py-2 text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
              @click="handleGenerateSubmit"
            >
              Generate
            </button>
            <button
              class="px-3 py-2 text-sm text-white rounded cursor-pointer transition-colors"
              :class="
                isGetAudioEnabled
                  ? 'bg-orange-500 hover:bg-orange-600'
                  : 'bg-gray-500 cursor-not-allowed '
              "
              @click="handleGetAudio"
              :disabled="!isGetAudioEnabled"
            >
              Get Audio
            </button>
          </div>

          <!-- 狀態和音檔區域 -->
          <div class="space-y-2">
            <div v-if="audioUrl" class="flex items-center justify-between w-full gap-2">
              <span
                class="flex-grow min-h-[32px] px-3 py-2 text-sm text-slate-200 bg-slate-600 rounded"
              >
                {{ singleGenerateResult }}
              </span>
              <a
                :href="audioUrl"
                :download="`${taskId || 'audio'}.wav`"
                class="px-3 py-2 text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
              >
                Download
              </a>
            </div>
            <div v-else class="flex items-center w-full">
              <span
                class="flex-grow min-h-[32px] px-3 py-2 text-sm text-slate-200 bg-slate-600 rounded"
              >
                {{ singleGenerateResult }}
              </span>
            </div>

            <!-- Audio player -->
            <audio v-if="audioUrl" controls class="w-full mt-2" :src="audioUrl">
              Your browser does not support the audio element.
            </audio>
          </div>
        </div>
      </div>
    </div>

    <div class="hidden md:flex flex-col w-1/3">
      <div
        class="flex flex-col flex-grow w-full text-lg text-slate-100 bg-slate-700 rounded-lg shadow-lg border border-slate-600"
      >
        <div class="flex items-start justify-between">
          <div
            class="px-3 py-1 text-sm text-slate-100 bg-slate-600 rounded shadow-lg border border-slate-500"
          >
            Generate logs
          </div>
          <button
            class="px-3 py-1 mt-3 mr-3 text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
            @click="handleCheckLogClick"
          >
            Check logs
          </button>
        </div>
        <div class="flex-grow h-[150px] m-3 bg-slate-600 rounded">
          <div class="h-full overflow-auto rounded">
            <template v-if="Array.isArray(logList)">
              <ul class="p-2 text-sm bg-slate-600 rounded">
                <li v-for="(logs, index) in logList" :key="logs" class="flex text-slate-200 py-1">
                  <span class="flex-none w-8 text-center">{{ index + 1 }}.</span>
                  <span class="flex-grow">{{ logs }}</span>
                </li>
              </ul>
            </template>
            <template v-else>
              <div class="p-3 text-sm text-slate-200 bg-slate-600 rounded">
                {{ logList }}
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { inject, ref, onMounted, onUnmounted, watch } from 'vue'
import type { Ref } from 'vue'
import axios from 'axios'
import UploadHandler from '@/components/Common/UploadHandler.vue'

// Single Generate page specific state
const singleText = ref('')
const selectedSpeaker = ref('')
const singleGenerateResult = ref('Ready to generate...')
const audioUrl = ref('')
const auditionAudioUrl = ref('')
const isServiceStarted = ref(false)
const isGetAudioEnabled = ref(false)
const autoRetryCount = ref(0)
const maxRetryCount = 3
let autoRetryInterval: ReturnType<typeof setInterval> | null = null
let taskIdDebounceTimer: ReturnType<typeof setTimeout> | null = null
let previousAudioUrl = ''
const speakerList = inject<Ref<string | string[]>>('speakerList')!
const speakerUploadFile = inject<Ref<File | null>>('speakerUploadFile')!
const speakerUploadResult = inject<Ref<string>>('speakerUploadResult')!
const isTooltipVisible = inject<Ref<boolean>>('isTooltipVisible')!
const isGenerateTipVisible = inject<Ref<boolean>>('isGenerateTipVisible')!
const tooltipX = inject<Ref<number>>('tooltipX')!
const tooltipY = inject<Ref<number>>('tooltipY')!
const logList = inject<Ref<string | string[]>>('logList')!
const taskId = inject<Ref<string>>('taskId')!

const handleSpeakerListClick = inject<() => Promise<void>>('handleSpeakerListClick')!
const handleSpeakerUploadClick = inject<() => Promise<void>>('handleSpeakerUploadClick')!
const showToolTip = inject<() => void>('showToolTip')!
const hideToolTip = inject<() => void>('hideToolTip')!
const updateTooltipPosition = inject<(event: MouseEvent) => void>('updateTooltipPosition')!
const showGenerateTip = inject<() => void>('showGenerateTip')!
const hideGenerateTip = inject<() => void>('hideGenerateTip')!
const updateGenerateTipPosition = inject<(event: MouseEvent) => void>('updateGenerateTipPosition')!
const handleCheckLogClick = inject<() => Promise<void>>('handleCheckLogClick')!

// Speaker selection
const selectSpeaker = async (speaker: string) => {
  selectedSpeaker.value = speaker
  auditionAudioUrl.value = ''

  // Call speaker audition API to get speaker audio
  if (taskId.value.trim()) {
    try {
      const response = await axios.get(
        `http://52.183.25.173:52010/speaker_audition?task_id=${taskId.value}&speaker_name=${speaker}`,
        {
          responseType: 'blob', // Set response type to blob
        },
      )

      if (response.data.type === 'application/json') {
        // Handle JSON response (error message)
        const text = await response.data.text()
        const json = JSON.parse(text)
        console.error('Speaker audition error:', json.message)
        auditionAudioUrl.value = json.message
        // Can display error message to user here
      } else {
        // Create audio URL
        const blob = new Blob([response.data], { type: 'audio/wav' })
        auditionAudioUrl.value = window.URL.createObjectURL(blob)
        console.log('Speaker audition loaded for:', speaker)
      }
    } catch (error) {
      console.error('Error loading speaker audition:', error)
      // Can display error message to user here
    }
  }

  console.log('Selected speaker:', speaker)
}

// Load speaker list
const loadSpeakerList = async () => {
  // Use handleSpeakerListClick from App.vue directly as it has more complete logic
  await handleSpeakerListClick()
}

// Start single generate service
const startSingleGenerateService = async () => {
  if (!taskId.value.trim() || isServiceStarted.value) return

  try {
    const formData = new FormData()
    formData.append('task_id', taskId.value)

    const response = await axios.post(
      'http://52.183.25.173:52010/start_single_generate_service',
      formData,
    )
    if (response.data.status === 'OK') {
      isServiceStarted.value = true
      console.log('Single generate service started')
    }
  } catch (error) {
    console.error('Error starting service:', error)
  }
}

// Stop single generate service
const stopSingleGenerateService = async () => {
  if (!taskId.value.trim() || !isServiceStarted.value) return

  try {
    const formData = new FormData()
    formData.append('task_id', taskId.value)

    const response = await axios.post(
      'http://52.183.25.173:52010/stop_single_generate_service',
      formData,
    )
    if (response.data.status === 'OK') {
      isServiceStarted.value = false
      console.log('Single generate service stopped')
    }
  } catch (error) {
    console.error('Error stopping service:', error)
  }
}

// Stop auto retry
const stopAutoRetry = () => {
  if (autoRetryInterval) {
    clearInterval(autoRetryInterval)
    autoRetryInterval = null
  }
  autoRetryCount.value = 0
}

// Auto get audio
const autoGetAudio = async () => {
  if (autoRetryCount.value >= maxRetryCount) {
    stopAutoRetry()
    singleGenerateResult.value = 'Auto get audio failed, please try again manually later'
    isGetAudioEnabled.value = true
    return
  }

  autoRetryCount.value++
  singleGenerateResult.value = `Attempting to get audio (${autoRetryCount.value}/${maxRetryCount})`

  try {
    const response = await axios.get(
      `http://52.183.25.173:52010/get_single_audio?task_id=${taskId.value}`,
      {
        responseType: 'blob',
      },
    )

    if (response.data.type === 'application/json') {
      // Handle JSON response (error or status message)
      const text = await response.data.text()
      JSON.parse(text) // Parse but don't store, just for format validation
      // Continue retrying
    } else {
      // Handle audio blob - successfully obtained
      const blob = new Blob([response.data], { type: 'audio/wav' })
      const newAudioUrl = window.URL.createObjectURL(blob)

      // Check if the new audio URL is the same as the previous one
      if (newAudioUrl === previousAudioUrl) {
        // Same audio file, continue retrying
        console.log('Same audio file detected, continuing retry...')
        return
      }

      // Different audio file, generation successful
      audioUrl.value = newAudioUrl
      previousAudioUrl = newAudioUrl
      singleGenerateResult.value = 'Audio generation successful!'
      stopAutoRetry()
      isGetAudioEnabled.value = true
    }
  } catch (error) {
    console.error('Auto retry error:', error)
    // Continue retrying
  }
}

// Submit inference
const handleGenerateSubmit = async () => {
  if (!taskId.value.trim() || !selectedSpeaker.value || !singleText.value.trim()) {
    singleGenerateResult.value = 'Please enter Task ID, select speaker and enter text'
    return
  }

  // Reset state
  stopAutoRetry()
  previousAudioUrl = audioUrl.value // Store current audio URL before resetting
  audioUrl.value = ''
  isGetAudioEnabled.value = false
  singleGenerateResult.value = 'Submitting generation request...'

  try {
    const formData = new FormData()
    formData.append('task_id', taskId.value)
    formData.append('speaker_name', selectedSpeaker.value)
    formData.append('text', singleText.value)

    const response = await axios.post('http://52.183.25.173:52010/single_generate', formData)
    if (response.data.status === 'OK') {
      singleGenerateResult.value =
        'Generation request submitted, will start audio retrieval in 5 seconds...'

      // Start auto retry
      autoRetryCount.value = 0
      autoRetryInterval = setInterval(autoGetAudio, 5000)

      // Wait 5 seconds before first attempt
      setTimeout(autoGetAudio, 5000)
    } else {
      singleGenerateResult.value = response.data.message || 'Failed to submit request'
      isGetAudioEnabled.value = true
    }
  } catch (error) {
    singleGenerateResult.value = 'Error submitting request'
    isGetAudioEnabled.value = true
    console.error('Error submitting generation:', error)
  }
}

// Get audio (manual)
const handleGetAudio = async () => {
  if (!taskId.value.trim()) {
    singleGenerateResult.value = 'Please enter Task ID'
    return
  }

  if (!isGetAudioEnabled.value) {
    return
  }

  singleGenerateResult.value = 'Getting audio...'
  audioUrl.value = ''
  try {
    const response = await axios.get(
      `http://52.183.25.173:52010/get_single_audio?task_id=${taskId.value}`,
      {
        responseType: 'blob',
      },
    )

    if (response.data.type === 'application/json') {
      // Handle JSON response (error or status message)
      const text = await response.data.text()
      const json = JSON.parse(text)
      singleGenerateResult.value = json.message || 'No audio available yet'
    } else {
      // Handle audio blob
      const blob = new Blob([response.data], { type: 'audio/wav' })
      audioUrl.value = window.URL.createObjectURL(blob)
      singleGenerateResult.value = 'Audio retrieved successfully!'
    }
  } catch (error) {
    singleGenerateResult.value = 'Error retrieving audio'
    console.error('Error getting audio:', error)
  }
}

// Page load handling
onMounted(async () => {
  // Try to load speaker list on initialization
  await loadSpeakerList()
  if (taskId.value.trim()) {
    await startSingleGenerateService()
  }
})

// Watch taskId changes and auto load speaker list (with debounce to prevent frequent calls)
watch(
  taskId,
  async (newTaskId, oldTaskId) => {
    // Clear previous timer
    if (taskIdDebounceTimer) {
      clearTimeout(taskIdDebounceTimer)
    }

    // Reset speaker related state
    selectedSpeaker.value = ''
    auditionAudioUrl.value = ''

    // Set new timer, execute after 1 second
    taskIdDebounceTimer = setTimeout(async () => {
      if (newTaskId && newTaskId.trim()) {
        // First load new speaker list and start new service
        await loadSpeakerList()
        isServiceStarted.value = false
        if (!isServiceStarted.value) {
          await startSingleGenerateService()
        }

        // If there's an old taskId and it's different from the new one, stop old service
        if (oldTaskId && oldTaskId.trim() && oldTaskId !== newTaskId) {
          try {
            const formData = new FormData()
            formData.append('task_id', oldTaskId)

            const response = await axios.post(
              'http://52.183.25.173:52010/stop_single_generate_service',
              formData,
            )
            if (response.data.status === 'OK') {
              console.log('Old single generate service stopped for taskId:', oldTaskId)
            }
          } catch (error) {
            console.error('Error stopping old service:', error)
          }
        }
      }
    }, 1000)
  },
  { immediate: false },
)

// Page unmount handling
onUnmounted(async () => {
  // Clear all timers
  if (taskIdDebounceTimer) {
    clearTimeout(taskIdDebounceTimer)
  }
  stopAutoRetry()
  await stopSingleGenerateService()
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
