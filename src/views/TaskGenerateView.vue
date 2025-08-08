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
            <template v-if="Array.isArray(speakerList)">
              <ul class="p-2 text-sm bg-slate-600 rounded">
                <li
                  v-for="(speaker, index) in speakerList"
                  :key="speaker"
                  class="flex items-center text-slate-200 py-1"
                >
                  <span class="flex-none w-8 text-center">{{ index + 1 }}.</span>
                  <span class="flex-grow">{{ speaker }}</span>
                </li>
              </ul>
            </template>
            <template v-else>
              <div class="p-3 text-sm text-slate-200 bg-slate-600 rounded text-center">
                {{ speakerList }}
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>

    <div class="flex flex-col w-full md:w-1/3">
      <div
        class="flex flex-col w-full text-lg text-slate-100 bg-slate-700 rounded-lg shadow-lg border border-slate-600"
      >
        <div class="flex items-center justify-between">
          <div
            class="px-3 py-1 text-sm text-slate-100 bg-slate-600 rounded shadow-lg border border-slate-500"
          >
            Prepare csv
          </div>
          <img
            src="@/assets/samples/exclamation.png"
            alt="Icon"
            class="hidden lg:block w-4 h-4 mt-3 mr-3 cursor-pointer"
            @mouseover="showTxtTip"
            @mouseleave="hideTxtTip"
            @mousemove="updateTxtTipPosition"
          />
          <transition name="fade">
            <div
              v-if="isTxtTipVisible"
              :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }"
              class="fixed z-50 p-2 text-slate-100 bg-slate-700 rounded shadow-lg border border-slate-600"
            >
              <img src="@/assets/samples/txt_sample.png" alt="Tooltip Image" />
            </div>
          </transition>
        </div>
        <div class="p-3 space-y-2">
          <div class="flex items-center gap-2">
            <button
              class="px-3 py-2 whitespace-nowrap text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
              @click="handleCSVClick"
            >
              CSV generate
            </button>
            <UploadHandler v-model="txtUploadFile" />
          </div>
          <div class="flex items-center gap-2 accent-blue-500">
            <label for="expansionRatio" class="text-sm whitespace-nowrap">Expansion Ratio:</label>
            <input
              type="range"
              min="1"
              max="3"
              step="0.1"
              v-model="expansionRatio"
              class="flex-grow"
            />
            <span class="text-sm w-8">{{ expansionRatio }}</span>
          </div>
          <div class="flex items-center gap-2">
            <div
              class="flex items-center flex-grow min-h-[32px] p-3 text-sm text-slate-200 bg-slate-600 rounded"
            >
              {{ csvUploadResult }}
            </div>
            <div v-if="downloadUrl" class="flex items-center">
              <a
                :href="downloadUrl"
                :download="`${taskId}.csv`"
                class="px-3 py-2 whitespace-nowrap text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
              >
                Download CSV
              </a>
            </div>
            <div v-else class="flex items-center">
              <button
                class="px-3 py-2 whitespace-nowrap text-sm text-slate-400 bg-slate-600 rounded opacity-50 cursor-not-allowed"
                disabled
              >
                Download CSV
              </button>
            </div>
          </div>
        </div>
      </div>
      <div
        class="flex flex-col flex-grow w-full mt-3 text-lg text-slate-100 bg-slate-700 rounded-lg shadow-lg border border-slate-600"
      >
        <div class="flex items-center justify-between">
          <div
            class="px-3 py-1 text-sm text-slate-100 bg-slate-600 rounded shadow-lg border border-slate-500"
          >
            Start Generation
          </div>
        </div>

        <div class="p-3 space-y-2">
          <div class="flex items-center gap-2">
            <label class="text-sm">Quality Check:</label>
            <input type="checkbox" v-model="qualityCheck" class="form-checkbox accent-blue-500" />
            <label class="px-2 py-1 text-xs text-slate-200 bg-slate-600 rounded">
              (*Check audio quality but may increase time)
            </label>
          </div>

          <div class="flex items-center gap-2 accent-blue-500">
            <label for="threadRatio" class="text-sm whitespace-nowrap">Thread number:</label>
            <input type="range" min="1" max="3" step="1" v-model="threadRatio" class="flex-grow" />
            <span class="text-sm w-8">{{ threadRatio }}</span>
          </div>

          <div class="flex items-center gap-2">
            <button
              class="px-3 py-2 whitespace-nowrap text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
              @click="handleThreadSuggestionClick"
            >
              Thread Suggestion
            </button>
            <span
              class="min-h-[32px] flex-grow px-3 py-2 text-sm text-slate-200 bg-slate-600 rounded"
              >{{ threadSuggestion }}</span
            >
          </div>

          <div class="flex items-center gap-2">
            <label class="text-sm whitespace-nowrap">Upload CSV:</label>
            <button
              class="px-3 py-2 text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
              @click="handleCheckCsvClick"
            >
              CSV check
            </button>
            <UploadHandler v-model="csvUploadFile" />
          </div>

          <div
            class="min-h-[32px] px-3 py-2 text-center text-sm text-slate-200 bg-slate-600 rounded"
          >
            {{ csvCheckResult }}
          </div>

          <div class="flex items-center justify-center">
            <div v-if="csvCheckResult == ' | format is correct. | '" class="flex items-center">
              <button
                class="py-2 px-3 text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
                @click="handlestartgenerateClick"
              >
                Start Generate
              </button>
            </div>
            <div v-else class="flex items-center">
              <button
                class="py-2 px-3 text-sm text-slate-400 bg-slate-600 rounded opacity-50 cursor-not-allowed"
                disabled
              >
                Start Generate
              </button>
            </div>
          </div>

          <div class="min-h-[32px] px-3 py-2 text-sm text-slate-200 bg-slate-600 rounded">
            {{ generateResult }}
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

      <div
        class="flex flex-col w-full mt-3 text-lg text-slate-100 bg-slate-700 rounded-lg shadow-lg border border-slate-600"
      >
        <div class="flex items-center justify-between">
          <div
            class="px-3 py-1 text-sm text-slate-100 bg-slate-600 rounded shadow-lg border border-slate-500"
          >
            Options
          </div>
        </div>
        <div class="p-3 space-y-2">
          <div class="flex items-center justify-between gap-2">
            <button
              class="px-3 py-2 text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
              @click="handlecancelClick"
            >
              Cancel task
            </button>
            <button
              class="px-3 py-2 text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
              @click="handleDeleteClick"
            >
              Delete task
            </button>
            <button
              class="px-3 py-2 text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
              @click="handleGetAudiosClick"
            >
              Get result
            </button>
          </div>
          <div class="flex items-center gap-2">
            <div v-if="downloadaudios" class="flex items-center justify-between w-full gap-2">
              <span
                class="flex-grow min-h-[32px] px-3 py-2 text-sm text-slate-200 bg-slate-600 rounded"
                >{{ optResult }}</span
              >
              <a
                :href="downloadaudios"
                :download="`${taskId}.zip`"
                class="px-3 py-2 text-sm text-white bg-orange-500 rounded hover:bg-orange-600 cursor-pointer transition-colors"
              >
                Download
              </a>
            </div>
            <div v-else class="flex items-center w-full">
              <span
                class="flex-grow min-h-[32px] px-3 py-2 text-sm text-slate-200 bg-slate-600 rounded"
                >{{ optResult }}</span
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { inject } from 'vue'
import type { Ref } from 'vue'
import UploadHandler from '@/components/Common/UploadHandler.vue'
const taskId = inject<Ref<string>>('taskId')!
const speakerUploadFile = inject<Ref<File | null>>('speakerUploadFile')!
const txtUploadFile = inject<Ref<File | null>>('txtUploadFile')!
const csvUploadFile = inject<Ref<File | null>>('csvUploadFile')!
const speakerUploadResult = inject<Ref<string>>('speakerUploadResult')!
const csvUploadResult = inject<Ref<string>>('csvUploadResult')!
const speakerList = inject<Ref<string | string[]>>('speakerList')!
const logList = inject<Ref<string | string[]>>('logList')!
const expansionRatio = inject<Ref<number>>('expansionRatio')!
const downloadUrl = inject<Ref<string>>('downloadUrl')!
const downloadaudios = inject<Ref<string>>('downloadaudios')!
const qualityCheck = inject<Ref<boolean>>('qualityCheck')!
const threadRatio = inject<Ref<number>>('threadRatio')!
const threadSuggestion = inject<Ref<string>>('threadSuggestion')!
const generateResult = inject<Ref<string>>('generateResult')!
const optResult = inject<Ref<string>>('optResult')!
const csvCheckResult = inject<Ref<string>>('csvCheckResult')!
const isTooltipVisible = inject<Ref<boolean>>('isTooltipVisible')!
const isTxtTipVisible = inject<Ref<boolean>>('isTxtTipVisible')!
const tooltipX = inject<Ref<number>>('tooltipX')!
const tooltipY = inject<Ref<number>>('tooltipY')!

// 注入所有需要的函數
const showToolTip = inject<() => void>('showToolTip')!
const hideToolTip = inject<() => void>('hideToolTip')!
const showTxtTip = inject<() => void>('showTxtTip')!
const hideTxtTip = inject<() => void>('hideTxtTip')!
const updateTooltipPosition = inject<(event: MouseEvent) => void>('updateTooltipPosition')!
const updateTxtTipPosition = inject<(event: MouseEvent) => void>('updateTxtTipPosition')!
const handleSpeakerUploadClick = inject<() => Promise<void>>('handleSpeakerUploadClick')!
const handleSpeakerListClick = inject<() => Promise<void>>('handleSpeakerListClick')!
const handleCSVClick = inject<() => Promise<void>>('handleCSVClick')!
const handleThreadSuggestionClick = inject<() => Promise<void>>('handleThreadSuggestionClick')!
const handleCheckCsvClick = inject<() => Promise<void>>('handleCheckCsvClick')!
const handlestartgenerateClick = inject<() => Promise<void>>('handlestartgenerateClick')!
const handleCheckLogClick = inject<() => Promise<void>>('handleCheckLogClick')!
const handlecancelClick = inject<() => Promise<void>>('handlecancelClick')!
const handleDeleteClick = inject<() => Promise<void>>('handleDeleteClick')!
const handleGetAudiosClick = inject<() => Promise<void>>('handleGetAudiosClick')!
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
