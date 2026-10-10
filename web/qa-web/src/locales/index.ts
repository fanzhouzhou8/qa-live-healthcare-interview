import { computed, ref } from 'vue'
import zhCN from './zh-CN'
import enUS from './en-US'

export type Locale = 'zh-CN' | 'en-US'

const messages = {
  'zh-CN': zhCN,
  'en-US': enUS,
} as const

const STORAGE_KEY = 'qa-web-locale'

function getInitialLocale(): Locale {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved === 'zh-CN' || saved === 'en-US') {
    return saved
  }
  return 'zh-CN'
}

const locale = ref<Locale>(getInitialLocale())

export function setLocale(next: Locale) {
  locale.value = next
  localStorage.setItem(STORAGE_KEY, next)
}

export function useI18n() {
  const t = computed(() => messages[locale.value])

  return {
    locale,
    setLocale,
    t,
  }
}
