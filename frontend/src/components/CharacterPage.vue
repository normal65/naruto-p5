<template>
  <div class="character-page">
    <!-- 顶部标题 -->
    <header class="char-header">
      <div class="char-header-left">
        <h1 class="char-title">CHARACTER <span class="highlight">CHRONICLES</span></h1>
        <p class="char-subtitle">火影忍者人物图鉴 - P5 Style</p>
      </div>
      <div class="header-actions">
        <button class="add-char-btn" @click="showAddModal = true">
          <span class="plus-icon">+</span>
          ADD NEW
        </button>
        <button class="delete-char-btn" :class="{ active: isDeleteMode }" @click="toggleDeleteMode">
          <span class="delete-icon">✕</span>
          {{ isDeleteMode ? 'EXIT DELETE' : 'DELETE MODE' }}
        </button>
      </div>
    </header>

    <!-- 人物卡片网格 -->
    <main class="char-grid-container">
      <div class="char-grid">
        <div
          v-for="(char, index) in characters"
          :key="char.id"
          class="char-card"
          @click="triggerCharacterTransition(char, index)"
        >
          <div class="char-card-inner">
            <button
              v-if="isDeleteMode"
              class="card-delete-btn"
              @click.stop="deleteCharacter(char.id)"
            >✕</button>
            <div class="char-card-image">
              <img :src="getImageUrl(char.image)" :alt="char.name" />
            </div>
            <div class="char-card-info">
              <div class="char-role">{{ char.role }}</div>
              <div class="char-name">{{ char.name }}</div>
              <div class="char-name-en">{{ char.nameEn }}</div>
            </div>
            <div class="char-card-action">>> VIEW</div>
          </div>
        </div>
      </div>
    </main>

    <!-- 斜切过渡动画遮罩 -->
    <div class="slash-overlay" :class="{ active: isTransitioning }">
      <!-- 左上红色三角 -->
      <div class="slash-panel slash-red"></div>
      <!-- 右下黑色三角 -->
      <div class="slash-panel slash-black"></div>
      <!-- 中间闪电分割线 -->
      <div class="slash-zigzag"></div>
      <!-- 中心图片卡牌 -->
      <div class="slash-card" :class="currentStyleClass">
        <!-- P5面具专属特效 -->
        <div class="p5-flash"></div>
        <div class="p5-shockwave"></div>
        <div class="p5-shockwave w2"></div>
        <div class="p5-shockwave w3"></div>
        <div class="slash-card-inner">
          <img :src="currentCharImg" class="slash-card-img" />
          <div class="slash-card-label">{{ selectedChar?.name }}</div>
        </div>
      </div>
      <!-- 右下角名字 -->
      <div class="slash-name-text">{{ selectedChar?.nameEn }}</div>
    </div>

    <!-- 人物详情弹窗 -->
    <div class="p5-modal-overlay" :class="{ active: isModalOpen }" @click.self="closeModal">
      <div class="p5-modal-card" v-if="selectedChar">
        <button class="close-btn" @click="closeModal">X</button>
        <div class="p5-modal-header">
          <span class="p5-badge">{{ selectedChar.role }}</span>
          <h2>{{ selectedChar.name }}</h2>
          <div class="char-name-en-large">{{ selectedChar.nameEn }}</div>
        </div>
        <div class="p5-modal-body">
          <p class="main-summary">{{ selectedChar.summary }}</p>
          <div class="char-tags">
            <span v-for="tag in selectedChar.tags" :key="tag" class="char-tag char-tag-clickable" @click="onTagClick(tag)">{{ tag }}</span>
          </div>
          <div class="char-quote">
            <div class="quote-icon">"</div>
            <p class="quote-text">{{ selectedChar.quotes }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加新人物弹窗 -->
    <div class="p5-modal-overlay" :class="{ active: showAddModal }" @click.self="closeAddModal">
      <div class="p5-modal-card add-modal">
        <button class="close-btn" @click="closeAddModal">X</button>
        <div class="p5-modal-header">
          <span class="p5-badge">NEW CHARACTER</span>
          <h2>添加新人物</h2>
        </div>
        <div class="p5-modal-body">
          <form @submit.prevent="addNewCharacter" class="add-form">
            <div class="form-row">
              <div class="form-group">
                <label>姓名 *</label>
                <input v-model="newChar.name" type="text" placeholder="漩涡鸣人" required />
              </div>
              <div class="form-group">
                <label>英文名 *</label>
                <input v-model="newChar.nameEn" type="text" placeholder="NARUTO UZUMAKI" required />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>角色定位 *</label>
                <input v-model="newChar.role" type="text" placeholder="第七代火影" required />
              </div>
              <div class="form-group">
                <label>过渡动画</label>
                <select v-model="newChar.transitionStyle">
                  <option value="0">Style 1 - 眼神杀斜切</option>
                  <option value="1">Style 2 - 分屏撕裂</option>
                  <option value="2">Style 3 - 上升过冲</option>
                  <option value="3">Style 4 - 星芒碎裂</option>
                </select>
              </div>
            </div>

            <!-- 图片上传区域 -->
            <div class="form-group">
              <label>角色图片 *</label>
              <div class="upload-area" @click="triggerFileInput" @drop.prevent="handleDrop" @dragover.prevent>
                <input
                  ref="fileInput"
                  type="file"
                  accept="image/*"
                  @change="handleFileSelect"
                  style="display: none"
                />
                <div v-if="!imagePreview" class="upload-placeholder">
                  <div class="upload-icon">+</div>
                  <p>点击选择图片 或 拖拽图片到此处</p>
                  <p class="upload-hint">支持 JPG、PNG、GIF、WebP</p>
                </div>
                <div v-else class="upload-preview">
                  <img :src="imagePreview" alt="预览" />
                  <button type="button" class="remove-img-btn" @click.stop="removeImage">X</button>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>人物简介 *</label>
              <textarea v-model="newChar.summary" placeholder="输入人物简介..." rows="3" required></textarea>
            </div>
            <div class="form-group">
              <label>标签（逗号分隔）</label>
              <input v-model="newChar.tags" type="text" placeholder="九尾人柱力, 七代火影, 仙人模式" />
            </div>
            <div class="form-group">
              <label>经典台词</label>
              <input v-model="newChar.quotes" type="text" placeholder="这就是我的忍道！" />
            </div>
            <button type="submit" class="submit-btn" :disabled="isUploading">
              <span v-if="isUploading">UPLOADING...</span>
              <span v-else>ADD CHARACTER</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const characters = ref([])
const selectedChar = ref(null)
const isTransitioning = ref(false)
const isModalOpen = ref(false)
const currentCharImg = ref('')
const currentStyleClass = ref('')

// 添加新人物相关
const showAddModal = ref(false)
const fileInput = ref(null)
const imagePreview = ref(null)
const selectedFile = ref(null)
const isUploading = ref(false)

// 删除模式相关
const isDeleteMode = ref(false)

const newChar = ref({
  name: '',
  nameEn: '',
  role: '',
  summary: '',
  tags: '',
  quotes: '',
  transitionStyle: '0'
})

// 5种过渡动画样式：佐助固定P5面具，其他随机
const p5MaskChars = ['SASUKE UCHIHA']
const randomStyles = ['style-slash', 'style-split', 'style-rise', 'style-shatter']

const pickStyle = (char) => {
  if (p5MaskChars.includes(char.nameEn)) return 'style-p5mask'
  return randomStyles[Math.floor(Math.random() * randomStyles.length)]
}

// 获取图片URL
const getImageUrl = (image) => {
  if (!image) return '/images/p5_1.jpg'
  if (image.startsWith('upload_') || image.startsWith('uploads/')) {
    return `/images/${image}`
  }
  return `/images/${image}`
}

onMounted(async () => {
  try {
    const res = await fetch('/api/characters')
    if (res.ok) {
      characters.value = await res.json()
    }
  } catch (err) {
    console.error('获取人物数据失败:', err)
  }
})

// 触发斜切过渡动画
const triggerCharacterTransition = (char, index) => {
  if (isDeleteMode.value) return
  currentCharImg.value = getImageUrl(char.image)
  currentStyleClass.value = pickStyle(char)
  selectedChar.value = char
  isTransitioning.value = true

  setTimeout(() => { isModalOpen.value = true }, 800)
  setTimeout(() => { isTransitioning.value = false }, 1500)
}

const closeModal = () => { isModalOpen.value = false }
const closeAddModal = () => {
  showAddModal.value = false
  resetForm()
}

const resetForm = () => {
  newChar.value = {
    name: '', nameEn: '', role: '', summary: '', tags: '', quotes: '', transitionStyle: '0'
  }
  imagePreview.value = null
  selectedFile.value = null
}

// 文件选择
const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (e) => {
  const file = e.target.files[0]
  if (file) processFile(file)
}

const handleDrop = (e) => {
  const file = e.dataTransfer.files[0]
  if (file) processFile(file)
}

const processFile = (file) => {
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件！')
    return
  }
  selectedFile.value = file
  const reader = new FileReader()
  reader.onload = (e) => { imagePreview.value = e.target.result }
  reader.readAsDataURL(file)
}

const removeImage = () => {
  imagePreview.value = null
  selectedFile.value = null
  if (fileInput.value) fileInput.value.value = ''
}

// 添加新人物
const addNewCharacter = async () => {
  if (!selectedFile.value) {
    alert('请选择角色图片！')
    return
  }

  isUploading.value = true
  const formData = new FormData()
  formData.append('name', newChar.value.name)
  formData.append('nameEn', newChar.value.nameEn)
  formData.append('role', newChar.value.role)
  formData.append('summary', newChar.value.summary)
  formData.append('tags', newChar.value.tags)
  formData.append('quotes', newChar.value.quotes)
  formData.append('image', selectedFile.value)

  try {
    const res = await fetch('/api/characters', {
      method: 'POST',
      body: formData
    })
    if (res.ok) {
      await fetchCharacters()
      closeAddModal()
    }
  } catch (err) {
    console.error('添加人物失败:', err)
  } finally {
    isUploading.value = false
  }
}

const fetchCharacters = async () => {
  const res = await fetch('/api/characters')
  if (res.ok) characters.value = await res.json()
}

// 删除模式切换
const toggleDeleteMode = () => {
  isDeleteMode.value = !isDeleteMode.value
}

// 删除人物
const deleteCharacter = async (charId) => {
  if (!confirm('确定要删除这个人物吗？')) return
  try {
    const res = await fetch(`/api/characters/${charId}`, { method: 'DELETE' })
    if (res.ok) {
      await fetchCharacters()
    }
  } catch (err) {
    console.error('删除人物失败:', err)
  }
}

// 标签点击 - 随机动画重新播放
const onTagClick = (tag) => {
  if (!selectedChar.value) return
  const char = selectedChar.value
  isModalOpen.value = false

  setTimeout(() => {
    currentCharImg.value = getImageUrl(char.image)
    currentStyleClass.value = pickStyle(char)
    selectedChar.value = char
    isTransitioning.value = true

    setTimeout(() => { isModalOpen.value = true }, 800)
    setTimeout(() => { isTransitioning.value = false }, 1500)
  }, 300)
}
</script>

<style scoped>
.character-page {
  background-color: #0c0c0c;
  color: #ffffff;
  font-family: 'Noto Sans SC', sans-serif;
  overflow: hidden;
  height: 100vh;
  width: 100vw;
  position: relative;
}

/* 顶部 */
.char-header {
  padding: 1.2rem 2rem;
  position: relative;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.char-title {
  font-family: 'Impact', sans-serif;
  font-size: 2.8rem;
  color: #fff;
  background-color: #dc2626;
  display: inline-block;
  padding: 0.4rem 1.5rem;
  transform: skew(-10deg) rotate(-2deg);
  border: 4px solid #fff;
  box-shadow: 8px 8px 0px #000;
}

.char-title .highlight {
  color: #000;
  background-color: #ffeb3b;
  padding: 0 0.5rem;
}

.char-subtitle {
  font-size: 0.9rem;
  color: #ffeb3b;
  margin-top: 6px;
  background-color: #000;
  display: inline-block;
  padding: 0.15rem 0.8rem;
  transform: skew(-5deg) translate(10px, 0);
  border: 2px solid #dc2626;
}

.add-char-btn {
  background-color: #dc2626;
  color: #fff;
  border: 4px solid #fff;
  padding: 0.8rem 1.5rem;
  font-family: 'Impact', sans-serif;
  font-size: 1.2rem;
  cursor: pointer;
  transform: skew(-8deg);
  box-shadow: 6px 6px 0px #ffeb3b;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.add-char-btn:hover {
  background-color: #ffeb3b;
  color: #000;
  transform: skew(-8deg) scale(1.08) translateY(-3px);
  box-shadow: 8px 8px 0px #dc2626;
}

.plus-icon { font-size: 1.5rem; font-weight: bold; }

/* 删除模式按钮 */
.delete-char-btn {
  background-color: #111;
  color: #fff;
  border: 4px solid #fff;
  padding: 0.8rem 1.5rem;
  font-family: 'Impact', sans-serif;
  font-size: 1.2rem;
  cursor: pointer;
  transform: skew(-8deg);
  box-shadow: 6px 6px 0px #666;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.delete-char-btn:hover {
  background-color: #dc2626;
  transform: skew(-8deg) scale(1.08) translateY(-3px);
  box-shadow: 8px 8px 0px #fff;
}

.delete-char-btn.active {
  background-color: #dc2626;
  border-color: #ffeb3b;
  box-shadow: 6px 6px 0px #ffeb3b;
}

.delete-icon { font-size: 1.2rem; font-weight: bold; }

/* 卡片上的删除按钮 */
.card-delete-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 20;
  background-color: #dc2626;
  color: #fff;
  border: 3px solid #fff;
  width: 32px;
  height: 32px;
  font-size: 1rem;
  font-family: 'Impact';
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 3px 3px 0px #000;
  transition: all 0.2s ease;
  transform: skew(-5deg);
}

.card-delete-btn:hover {
  background-color: #fff;
  color: #dc2626;
  transform: skew(-5deg) scale(1.2);
  box-shadow: 4px 4px 0px #dc2626;
}

/* 网格 */
.char-grid-container {
  position: relative;
  z-index: 5;
  width: 100vw;
  height: calc(100vh - 100px);
  overflow-y: auto;
  padding: 1rem 3rem 3rem;
}

.char-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.8rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* 卡片 */
.char-card {
  cursor: pointer;
  transform: skew(-3deg);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.char-card:hover {
  transform: skew(-3deg) scale(1.05) translateY(-10px);
}

.char-card-inner {
  background-color: #111;
  border: 4px solid #fff;
  overflow: hidden;
  box-shadow: 8px 8px 0px #dc2626;
  transition: all 0.3s ease;
  position: relative;
}

.char-card:hover .char-card-inner {
  border-color: #ffeb3b;
  box-shadow: 12px 12px 0px #ffeb3b;
}

.char-card-image {
  width: 100%;
  height: 280px;
  overflow: hidden;
  background-color: #000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.char-card-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transform: scale(1);
  transition: transform 0.4s ease;
}

.char-card:hover .char-card-image img { transform: scale(1.08); }

.char-card-info { padding: 0.8rem 1rem; }

.char-role {
  font-size: 0.65rem;
  background-color: #dc2626;
  color: #fff;
  padding: 0.2rem 0.5rem;
  display: inline-block;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.4rem;
}

.char-name {
  font-family: 'Impact', sans-serif;
  font-size: 1.4rem;
  color: #ffeb3b;
  margin-bottom: 0.2rem;
}

.char-name-en {
  font-family: 'Impact', sans-serif;
  font-size: 0.7rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.char-card-action {
  background-color: #000;
  padding: 0.4rem;
  text-align: right;
  font-family: 'Impact';
  font-size: 0.75rem;
  color: #aaa;
  border-top: 2px solid #333;
}

.char-card:hover .char-card-action {
  color: #ffeb3b;
  background-color: #1a1a1a;
}

/* =======================================================
   ★★★ 斜切过渡动画 - 核心效果 ★★★
   ======================================================= */
.slash-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 100;
  pointer-events: none;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.15s ease;
}

.slash-overlay.active {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}

/* 左上红色面板 */
.slash-panel {
  position: absolute;
  width: 100%; height: 100%;
  transition: transform 0.5s cubic-bezier(0.19, 1, 0.22, 1);
}

.slash-red {
  background-color: #dc2626;
  clip-path: polygon(0 0, 65% 0, 35% 100%, 0% 100%);
  transform: translateX(-110%);
}

.slash-overlay.active .slash-red {
  transform: translateX(0);
}

/* 右下黑色面板 */
.slash-black {
  background-color: #111;
  clip-path: polygon(65% 0, 100% 0, 100% 100%, 35% 100%);
  transform: translateX(110%);
  transition-delay: 0.05s;
}

.slash-overlay.active .slash-black {
  transform: translateX(0);
}

/* 中间闪电分割线 */
.slash-zigzag {
  position: absolute;
  top: -5vh;
  left: 33%;
  width: 60px;
  height: 110vh;
  background-color: #ffeb3b;
  clip-path: polygon(20% 0%, 80% 5%, 30% 10%, 70% 15%, 20% 20%, 80% 25%, 30% 30%, 70% 35%, 20% 40%, 80% 45%, 30% 50%, 70% 55%, 20% 60%, 80% 65%, 30% 70%, 70% 75%, 20% 80%, 80% 85%, 30% 90%, 70% 95%, 20% 100%, 80% 100%, 100% 100%, 0% 100%, 0% 0%);
  transform: scaleX(0) skewX(-15deg);
  transform-origin: top left;
  transition: transform 0.4s cubic-bezier(0.19, 1, 0.22, 1) 0.25s;
  z-index: 2;
  box-shadow: 8px 0px 0px #000;
}

.slash-overlay.active .slash-zigzag {
  transform: scaleX(1) skewX(-15deg);
}

/* 中心卡牌 */
.slash-card {
  position: absolute;
  top: 50%; left: 50%;
  z-index: 5;
  opacity: 0;
  transform: translate(-50%, -50%) scale(0) rotate(-45deg);
  transition: transform 0.55s cubic-bezier(0.175, 0.885, 0.32, 1.275) 0.3s, opacity 0.3s ease 0.3s;
}

.slash-overlay.active .slash-card {
  opacity: 1;
}

.slash-card-inner {
  background-color: #000;
  border: 8px solid #fff;
  box-shadow: 20px 20px 0px #dc2626, -10px -10px 0px #000;
  overflow: hidden;
  max-width: 55vw;
  max-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.slash-card-img {
  display: block;
  max-width: 100%;
  max-height: 75vh;
  object-fit: contain;
}

/* =======================================================
   Style 1: 眼神杀斜切 - 从左上旋转飞入
   ======================================================= */
.slash-card.style-slash {
  transform: translate(-120%, -120%) scale(0.3) rotate(-90deg);
}

.slash-overlay.active .slash-card.style-slash {
  transform: translate(-50%, -50%) scale(1) rotate(-3deg);
  transition: transform 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) 0.25s, opacity 0.2s ease 0.25s;
}

/* =======================================================
   Style 2: 分屏撕裂 - 从左侧高速撞入
   ======================================================= */
.slash-card.style-split {
  transform: translate(-150%, -50%) scale(0.6) rotate(15deg);
}

.slash-overlay.active .slash-card.style-split {
  transform: translate(-50%, -50%) scale(1) rotate(-2deg);
  transition: transform 0.5s cubic-bezier(0.19, 1, 0.22, 1) 0.2s, opacity 0.2s ease 0.2s;
}

/* =======================================================
   Style 3: 上升过冲 - 从下方弹射上来
   ======================================================= */
.slash-card.style-rise {
  transform: translate(-50%, 120%) scale(0.5) rotate(8deg);
}

.slash-overlay.active .slash-card.style-rise {
  transform: translate(-50%, -50%) scale(1) rotate(-4deg);
  transition: transform 0.65s cubic-bezier(0.34, 1.56, 0.64, 1) 0.2s, opacity 0.2s ease 0.2s;
}

/* =======================================================
   Style 4: 星芒碎裂 - 从超大缩爆裂回
   ======================================================= */
.slash-card.style-shatter {
  transform: translate(-50%, -50%) scale(6) rotate(45deg);
}

.slash-overlay.active .slash-card.style-shatter {
  transform: translate(-50%, -50%) scale(1) rotate(-2deg);
  transition: transform 0.55s cubic-bezier(0.175, 0.885, 0.32, 1.275) 0.2s, opacity 0.2s ease 0.2s;
}

/* =======================================================
   Style 5: P5面具 - 佐助专属！中心爆裂 + 红色冲击波
   ======================================================= */
.slash-card.style-p5mask {
  transform: translate(-50%, -50%) scale(0) rotate(0deg);
  z-index: 10;
}

.slash-overlay.active .slash-card.style-p5mask {
  transform: translate(-50%, -50%) scale(1) rotate(-3deg);
  transition: transform 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s, opacity 0.2s ease 0.3s;
}

/* P5面具 - 红色冲击波光圈 */
.slash-card.style-p5mask .p5-shockwave {
  position: absolute;
  top: 50%; left: 50%;
  width: 200px; height: 200px;
  border: 6px solid #dc2626;
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  z-index: -1;
  pointer-events: none;
}

.slash-overlay.active .slash-card.style-p5mask .p5-shockwave {
  animation: p5-shockwave-pulse 0.8s cubic-bezier(0.19, 1, 0.22, 1) 0.3s forwards;
}

.slash-card.style-p5mask .p5-shockwave.w2 {
  animation-delay: 0.45s !important;
}

.slash-card.style-p5mask .p5-shockwave.w3 {
  animation-delay: 0.6s !important;
}

@keyframes p5-shockwave-pulse {
  0% { transform: translate(-50%, -50%) scale(0); opacity: 1; border-width: 8px; }
  100% { transform: translate(-50%, -50%) scale(5); opacity: 0; border-width: 1px; }
}

/* P5面具 - 背景红色爆炸闪光 */
.slash-card.style-p5mask .p5-flash {
  position: absolute;
  top: 50%; left: 50%;
  width: 100px; height: 100px;
  background: radial-gradient(circle, #dc2626 0%, #ff6b35 30%, transparent 70%);
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(0);
  z-index: -1;
  pointer-events: none;
}

.slash-overlay.active .slash-card.style-p5mask .p5-flash {
  animation: p5-flash-burst 0.5s cubic-bezier(0.19, 1, 0.22, 1) 0.25s forwards;
}

@keyframes p5-flash-burst {
  0% { transform: translate(-50%, -50%) scale(0); opacity: 1; }
  50% { opacity: 1; }
  100% { transform: translate(-50%, -50%) scale(8); opacity: 0; }
}

/* P5面具 - 斜向红色条纹扫过 */
.slash-overlay .slash-card.style-p5mask::after {
  content: '';
  position: absolute;
  top: -100%; left: -100%;
  width: 300%; height: 300%;
  background: repeating-linear-gradient(
    -45deg,
    transparent 0px,
    transparent 30px,
    rgba(220, 38, 38, 0.15) 30px,
    rgba(220, 38, 38, 0.15) 60px
  );
  opacity: 0;
  z-index: -1;
  pointer-events: none;
  transform: translateX(-100%);
}

.slash-overlay.active .slash-card.style-p5mask::after {
  animation: p5-stripes-sweep 0.6s ease 0.35s forwards;
}

@keyframes p5-stripes-sweep {
  0% { transform: translateX(-100%); opacity: 0; }
  30% { opacity: 1; }
  100% { transform: translateX(0%); opacity: 1; }
}

/* P5面具 - 卡牌额外阴影特效 */
.slash-overlay.active .slash-card.style-p5mask .slash-card-inner {
  box-shadow:
    0 0 0 4px #dc2626,
    0 0 0 8px #fff,
    0 0 40px rgba(220, 38, 38, 0.6),
    20px 20px 0px #dc2626,
    -10px -10px 0px #000;
}

.slash-card-label {
  position: absolute;
  bottom: -12px; left: 50%;
  transform: translateX(-50%) rotate(2deg);
  background-color: #ffeb3b;
  color: #000;
  padding: 0.3rem 2rem;
  font-family: 'Impact', sans-serif;
  font-weight: bold;
  font-size: 1.2rem;
  border: 3px solid #000;
  box-shadow: 5px 5px 0px #dc2626;
  white-space: nowrap;
  letter-spacing: 2px;
}

.slash-name-text {
  position: absolute;
  bottom: 8%; right: 5%;
  font-family: 'Impact', sans-serif;
  font-size: 2.5rem;
  color: #ffeb3b;
  text-shadow: 4px 4px 0px #000;
  z-index: 4;
  transform: rotate(-5deg) scale(0);
  transition: transform 0.3s ease 0.5s;
  white-space: nowrap;
  background-color: #000;
  padding: 0.5rem 1.5rem;
  border: 3px solid #fff;
}

.slash-overlay.active .slash-name-text {
  transform: rotate(-5deg) scale(1);
}

/* =======================================================
   弹窗样式
   ======================================================= */
.p5-modal-overlay {
  position: fixed; top: 0; left: 0;
  width: 100vw; height: 100vh;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex; align-items: center; justify-content: center;
  z-index: 90;
  opacity: 0; pointer-events: none;
  transition: opacity 0.3s ease;
}

.p5-modal-overlay.active { opacity: 1; pointer-events: auto; }

.p5-modal-card {
  background-color: #111;
  border: 5px solid #fff;
  width: 80%; max-width: 650px;
  max-height: 85vh; overflow-y: auto;
  padding: 2rem;
  position: relative;
  transform: scale(0.8) rotate(-5deg);
  box-shadow: 15px 15px 0px #dc2626;
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.2);
}

.p5-modal-overlay.active .p5-modal-card {
  transform: scale(1) rotate(-2deg);
}

.close-btn {
  position: absolute; top: -15px; right: -15px;
  background-color: #dc2626; color: #fff;
  border: 3px solid #fff;
  font-family: 'Impact'; font-size: 1.5rem;
  width: 45px; height: 45px;
  cursor: pointer;
  box-shadow: 4px 4px 0px #000;
  transform: rotate(15deg);
  transition: all 0.2s ease;
}

.close-btn:hover { background-color: #fff; color: #000; transform: rotate(0deg) scale(1.1); }

.p5-modal-header { border-bottom: 4px solid #dc2626; padding-bottom: 1rem; margin-bottom: 1.2rem; }

.p5-badge {
  background-color: #ffeb3b; color: #000;
  padding: 0.3rem 0.8rem; font-weight: bold;
  display: inline-block; transform: skew(-10deg); margin-bottom: 0.5rem;
}

.p5-modal-header h2 { font-family: 'Impact', sans-serif; font-size: 2rem; color: #fff; }
.char-name-en-large { font-family: 'Impact', sans-serif; font-size: 0.9rem; color: #888; text-transform: uppercase; letter-spacing: 3px; margin-top: 0.3rem; }
.main-summary { font-size: 1rem; line-height: 1.7; margin-bottom: 1.2rem; background-color: #1a1a1a; padding: 1rem; border-left: 5px solid #dc2626; color: #ddd; }

.char-tags { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-bottom: 1.2rem; }

.char-tag {
  background-color: #000; color: #ffeb3b;
  padding: 0.3rem 0.8rem; border: 2px solid #ffeb3b;
  font-family: 'Impact'; font-size: 0.8rem;
  transform: skew(-5deg); box-shadow: 3px 3px 0px #dc2626;
}

.char-tag-clickable {
  cursor: pointer;
  transition: all 0.2s ease;
}

.char-tag-clickable:hover {
  background-color: #dc2626;
  color: #fff;
  border-color: #fff;
  transform: skew(-5deg) scale(1.1);
  box-shadow: 5px 5px 0px #ffeb3b;
}

.char-quote { background-color: #000; border: 3px solid #dc2626; padding: 1.2rem; position: relative; transform: skew(-2deg); }
.quote-icon { position: absolute; top: -15px; left: 15px; font-family: 'Impact'; font-size: 3.5rem; color: #dc2626; line-height: 1; }
.quote-text { font-style: italic; font-size: 1.1rem; color: #fff; padding-left: 1.5rem; line-height: 1.6; }

/* =======================================================
   添加人物表单
   ======================================================= */
.add-modal { max-width: 650px; }

.add-form { display: flex; flex-direction: column; gap: 1rem; }

.form-row { display: flex; gap: 1rem; }

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-family: 'Impact', sans-serif;
  font-size: 0.9rem;
  color: #ffeb3b;
  margin-bottom: 0.3rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.form-group input, .form-group select, .form-group textarea {
  background-color: #000;
  border: 3px solid #fff;
  color: #fff;
  padding: 0.7rem;
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 0.95rem;
  transform: skew(-3deg);
  transition: all 0.3s ease;
}

.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
  outline: none;
  border-color: #ffeb3b;
  box-shadow: 4px 4px 0px #dc2626;
}

.form-group textarea { resize: none; }

/* 图片上传区域 */
.upload-area {
  border: 3px dashed #fff;
  background-color: #000;
  padding: 1rem;
  cursor: pointer;
  transform: skew(-3deg);
  transition: all 0.3s ease;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-area:hover {
  border-color: #ffeb3b;
  box-shadow: 4px 4px 0px #dc2626;
}

.upload-placeholder {
  text-align: center;
  color: #888;
}

.upload-icon {
  font-size: 3rem;
  color: #dc2626;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.upload-hint {
  font-size: 0.75rem;
  color: #666;
  margin-top: 0.3rem;
}

.upload-preview {
  position: relative;
  width: 100%;
}

.upload-preview img {
  width: 100%;
  max-height: 150px;
  object-fit: cover;
  border: 2px solid #fff;
}

.remove-img-btn {
  position: absolute;
  top: -10px; right: -10px;
  background-color: #dc2626;
  color: #fff;
  border: 2px solid #fff;
  width: 25px; height: 25px;
  font-family: 'Impact';
  font-size: 1rem;
  cursor: pointer;
  border-radius: 0;
}

.submit-btn {
  background-color: #dc2626;
  color: #fff;
  border: 4px solid #fff;
  padding: 1rem 2rem;
  font-family: 'Impact', sans-serif;
  font-size: 1.3rem;
  cursor: pointer;
  transform: skew(-8deg);
  box-shadow: 6px 6px 0px #ffeb3b;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  background-color: #ffeb3b;
  color: #000;
  transform: skew(-8deg) scale(1.05);
  box-shadow: 8px 8px 0px #dc2626;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
