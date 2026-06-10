<template>
  <div class="p5-app">
    <!-- 主页面：重大事件树状图 -->
    <template v-if="currentPage === 'events'">
      <!-- 背景斜线条纹 -->
      <div class="p5-bg-strips"></div>
      <div class="p5-star-decor">★</div>

      <!-- 顶部标题 -->
      <header class="p5-header">
        <h1 class="p5-title">NARUTO <span class="highlight">CHRONICLES</span></h1>
        <p class="p5-subtitle">火影忍者重大历史事件图鉴 - P5 Style</p>
      </header>

      <!-- 横向轴布局 -->
      <main class="tree-container">
        <div class="tree-wrapper">
          <div
            v-for="event in events"
            :key="event.id"
            class="tree-node"
            @click="triggerTransition(event)"
          >
            <div class="node-card">
              <div class="node-period">{{ event.period }}</div>
              <div class="node-title">{{ event.title }}</div>
              <div class="node-action">>> ENTER</div>
            </div>
          </div>
        </div>
      </main>

      <!-- P5 全自适应 & 四大招牌斩击动作遮罩 -->
      <div
        class="p5-transition-mask"
        :class="[{ active: isTransitioning }, currentTransitionStyle, currentLayout.align]"
      >
        <div class="base-slice slice-red"></div>
        <div class="base-slice slice-black"></div>

        <div class="p5-adaptive-container" v-if="currentTransitionImg">
          <template v-if="currentTransitionStyle === 'style-1'">
            <div class="eye-slash-back-yellow"></div>
            <div class="eye-slash-back-red"></div>
            <div class="p5-perfect-card" :style="{ '--card-rotate': currentLayout.rotate, '--card-skew': currentLayout.skew }">
              <img :src="currentTransitionImg" class="p5-perfect-img" alt="Slash" />
              <div class="p5-perfect-tape">{{ currentLayout.tapeText }}</div>
            </div>
          </template>
          <template v-else-if="currentTransitionStyle === 'style-2'">
            <div class="split-left-panel"></div>
            <div class="split-zigzag-line"></div>
            <div class="p5-split-right-card" :style="{ '--card-rotate': currentLayout.rotate, '--card-skew': currentLayout.skew }">
              <img :src="currentTransitionImg" class="p5-split-img" alt="Split Screen" />
              <div class="p5-perfect-tape">{{ currentLayout.tapeText }}</div>
            </div>
          </template>
          <template v-else-if="currentTransitionStyle === 'style-3'">
            <div class="op-layer-red-bg"></div>
            <div class="p5-perfect-card" :style="{ '--card-rotate': currentLayout.rotate, '--card-skew': currentLayout.skew }">
              <img :src="currentTransitionImg" class="p5-perfect-img" alt="OP style" />
              <div class="p5-perfect-tape">{{ currentLayout.tapeText }}</div>
            </div>
          </template>
          <template v-else-if="currentTransitionStyle === 'style-4'">
            <div class="shatter-shard-star shard-top-left"></div>
            <div class="shatter-shard-star shard-bottom-right"></div>
            <div class="p5-perfect-card" :style="{ '--card-rotate': currentLayout.rotate, '--card-skew': currentLayout.skew }">
              <img :src="currentTransitionImg" class="p5-perfect-img" alt="Shatter" />
              <div class="p5-perfect-tape">{{ currentLayout.tapeText }}</div>
            </div>
          </template>
        </div>

        <div class="slice-text">{{ selectedEvent?.title || 'LOADING...' }}</div>
      </div>

      <!-- P5 样式弹出窗口 -->
      <div class="p5-modal-overlay" :class="{ active: isModalOpen }" @click.self="closeModal">
        <div class="p5-modal-card" v-if="selectedEvent">
          <button class="close-btn" @click="closeModal">X</button>
          <div class="p5-modal-header">
            <span class="p5-badge">{{ selectedEvent.period }}</span>
            <h2>{{ selectedEvent.title }}</h2>
          </div>
          <div class="p5-modal-body">
            <p class="main-summary">{{ selectedEvent.summary }}</p>
            <div class="sub-nodes-container">
              <h3 class="sub-section-title">// 关键节点事件</h3>
              <div class="sub-nodes-list">
                <div v-for="sub in selectedEvent.children" :key="sub.id" class="sub-node-box">
                  <h4>{{ sub.title }}</h4>
                  <p>{{ sub.detail }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- 人物简介页面 -->
    <template v-else-if="currentPage === 'characters'">
      <CharacterPage />
    </template>

    <!-- ESC菜单按钮（始终显示在右下角） -->
    <div class="esc-menu-trigger" @click="toggleMenu">
      <span class="esc-icon">ESC</span>
      <span class="esc-label">MENU</span>
    </div>

    <!-- ESC菜单遮罩 -->
    <div class="p5-esc-menu-overlay" :class="{ active: isMenuOpen }" @click.self="toggleMenu">
      <div class="p5-esc-menu-panel">
        <div class="menu-panel-red"></div>
        <div class="menu-panel-black"></div>
        <div class="menu-panel-zigzag"></div>
      </div>

      <div class="p5-esc-menu-image">
        <img :src="menuBgImage" class="menu-display-img" alt="Menu Image" />
      </div>

      <div class="p5-esc-menu-items">
        <div
          v-for="(item, index) in menuItems"
          :key="item.id"
          class="menu-item"
          :class="{ active: currentMenuIndex === index }"
          @mouseenter="currentMenuIndex = index"
          @click="selectMenuItem(item)"
        >
          <span class="menu-item-number">0{{ index + 1 }}</span>
          <span class="menu-item-title">{{ item.title }}</span>
          <span class="menu-item-subtitle">{{ item.subtitle }}</span>
        </div>
      </div>

      <div class="p5-esc-hint">
        <span class="esc-key-hint">ESC</span> TO CLOSE
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import CharacterPage from './components/CharacterPage.vue'

const currentPage = ref('events')
const events = ref([])
const selectedEvent = ref(null)
const isTransitioning = ref(false)
const isModalOpen = ref(false)
const isMenuOpen = ref(false)
const currentMenuIndex = ref(0)
const currentTransitionImg = ref('')
const currentTransitionStyle = ref('')

const menuItems = ref([
  { id: 'events', title: '重大事件', subtitle: 'MAJOR EVENTS', type: 'events' },
  { id: 'characters', title: '人物简介', subtitle: 'CHARACTERS', type: 'characters' }
])

const menuBgImage = '/images/p5_1.jpg'

const layoutMap = {
  arc_1: { align: 'align-left', rotate: '-4deg', skew: '-10deg', tapeText: '★ AKATSUKI' },
  arc_2: { align: 'align-right', rotate: '3deg', skew: '-8deg', tapeText: '★ SEVENTH' },
  arc_3: { align: 'align-center', rotate: '-2deg', skew: '-10deg', tapeText: '★ CHRONICLE' },
  arc_4: { align: 'align-left', rotate: '4deg', skew: '-8deg', tapeText: '★ PAIN' },
  arc_5: { align: 'align-center', rotate: '-3deg', skew: '-10deg', tapeText: '★ WAR' }
}

const currentLayout = ref({ align: 'align-center', rotate: '-2deg', skew: '-10deg', tapeText: '★ NARUTO' })

// ESC键处理 - 使用 document 级别监听，最可靠
const handleKeyDown = (e) => {
  if (e.key === 'Escape') {
    e.preventDefault()
    toggleMenu()
  }
}

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
  if (isMenuOpen.value) {
    currentMenuIndex.value = 0
  }
}

const selectMenuItem = (item) => {
  currentPage.value = item.type
  toggleMenu()
}

const closeModal = () => {
  isModalOpen.value = false
}

onMounted(async () => {
  // 在 document 级别监听键盘事件，不依赖焦点
  document.addEventListener('keydown', handleKeyDown)

  try {
    const res = await fetch('/api/events')
    if (res.ok) {
      events.value = await res.json()
    }
  } catch (err) {
    console.error('网络请求异常:', err)
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})

const triggerTransition = (event) => {
  currentTransitionImg.value = `/images/${event.id}.jpg`
  currentLayout.value = layoutMap[event.id] || {
    align: 'align-center', rotate: '-2deg', skew: '-10deg', tapeText: '★ NARUTO'
  }

  const styles = ['style-1', 'style-2', 'style-3', 'style-4']
  currentTransitionStyle.value = styles[Math.floor(Math.random() * styles.length)]

  isTransitioning.value = true
  selectedEvent.value = event

  setTimeout(() => { isModalOpen.value = true }, 650)
  setTimeout(() => { isTransitioning.value = false }, 1500)
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Impact&family=Noto+Sans+SC:wght@700;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.p5-app {
  background-color: #0c0c0c;
  color: #ffffff;
  font-family: 'Noto Sans SC', sans-serif;
  overflow: hidden;
  height: 100vh;
  width: 100vw;
  position: relative;
}

.p5-bg-strips {
  position: absolute;
  top: 0; left: 0;
  width: 200vw; height: 200vh;
  background: repeating-linear-gradient(-45deg, #111 0px, #111 40px, #1a1a1a 40px, #1a1a1a 80px);
  z-index: 1;
  transform: rotate(-5deg) translate(-10%, -10%);
}

.p5-star-decor {
  position: absolute;
  bottom: 5%; right: 5%;
  font-size: 8rem;
  color: #dc2626;
  opacity: 0.15;
  font-family: 'Impact';
  z-index: 1;
  transform: rotate(15deg);
  user-select: none;
}

.p5-header {
  padding: 2rem;
  position: relative;
  z-index: 10;
}

.p5-title {
  font-family: 'Impact', sans-serif;
  font-size: 3.5rem;
  color: #fff;
  background-color: #dc2626;
  display: inline-block;
  padding: 0.5rem 2rem;
  transform: skew(-10deg) rotate(-2deg);
  border: 4px solid #fff;
  box-shadow: 8px 8px 0px #000;
}

.p5-title .highlight {
  color: #000;
  background-color: #fff;
  padding: 0 0.5rem;
}

.p5-subtitle {
  font-size: 1.1rem;
  color: #ffeb3b;
  margin-top: 10px;
  background-color: #000;
  display: inline-block;
  padding: 0.2rem 1rem;
  transform: skew(-5deg) translate(15px, 0);
  border: 2px solid #dc2626;
}

.tree-container {
  position: relative;
  z-index: 5;
  width: 100vw;
  height: calc(100vh - 180px);
  overflow-x: auto;
  overflow-y: hidden;
  display: flex;
  align-items: center;
  padding: 0 10%;
}

.tree-wrapper {
  display: flex;
  align-items: center;
  gap: 150px;
  position: relative;
}

.tree-wrapper::before {
  content: '';
  position: absolute;
  top: 50%; left: 0;
  width: 100%; height: 8px;
  background-color: #fff;
  border: 2px solid #000;
  transform: translateY(-50%) skew(-10deg);
  z-index: 1;
}

.tree-node {
  position: relative;
  z-index: 2;
  cursor: pointer;
}

.node-card {
  background-color: #000;
  border: 4px solid #fff;
  padding: 1.5rem;
  width: 250px;
  transform: skew(-8deg);
  box-shadow: 8px 8px 0px #dc2626;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.node-card:hover {
  background-color: #dc2626;
  box-shadow: 8px 8px 0px #fff;
  transform: skew(-8deg) scale(1.08) translateY(-10px);
}

.node-card:hover .node-title { color: #fff; }
.node-card:hover .node-period { background-color: #fff; color: #000; }

.node-period {
  font-size: 0.8rem;
  background-color: #dc2626;
  color: #fff;
  padding: 0.2rem 0.5rem;
  display: inline-block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.node-title {
  font-size: 1.5rem;
  color: #ffeb3b;
  margin-bottom: 0.5rem;
}

.node-action {
  font-size: 0.8rem;
  text-align: right;
  color: #aaa;
  text-transform: uppercase;
  font-family: 'Impact';
}

/* =======================================================
   右下角 ESC 菜单触发按钮
   ======================================================= */
.esc-menu-trigger {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 150;
  background-color: #dc2626;
  border: 4px solid #fff;
  padding: 0.8rem 1.2rem;
  cursor: pointer;
  transform: skew(-8deg);
  box-shadow: 6px 6px 0px #ffeb3b;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.esc-menu-trigger:hover {
  background-color: #ffeb3b;
  transform: skew(-8deg) scale(1.1) translateY(-3px);
  box-shadow: 8px 8px 0px #dc2626;
}

.esc-icon {
  font-family: 'Impact', sans-serif;
  font-size: 1.3rem;
  color: #fff;
  background-color: #000;
  padding: 0.2rem 0.5rem;
  border: 2px solid #fff;
}

.esc-menu-trigger:hover .esc-icon {
  color: #000;
  background-color: #dc2626;
}

.esc-label {
  font-family: 'Impact', sans-serif;
  font-size: 1.1rem;
  color: #fff;
}

.esc-menu-trigger:hover .esc-label {
  color: #000;
}

/* =======================================================
   ESC菜单
   ======================================================= */
.p5-esc-menu-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 200;
  pointer-events: none;
  visibility: hidden;
  overflow: hidden;
}

.p5-esc-menu-overlay.active {
  visibility: visible;
  pointer-events: auto;
}

.p5-esc-menu-panel {
  position: absolute;
  top: 0; left: 0;
  width: 60vw; height: 100vh;
  transform: translateX(-100%);
  transition: transform 0.5s cubic-bezier(0.19, 1, 0.22, 1);
}

.p5-esc-menu-overlay.active .p5-esc-menu-panel {
  transform: translateX(0);
}

.menu-panel-red {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: #dc2626;
  clip-path: polygon(0 0, 100% 0, 70% 100%, 0% 100%);
}

.menu-panel-black {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: #111;
  clip-path: polygon(70% 0, 100% 0, 100% 100%, 40% 100%);
  border-left: 8px solid #ffeb3b;
}

.menu-panel-zigzag {
  position: absolute;
  top: 0; left: 70%;
  width: 15px; height: 100%;
  background-color: #ffeb3b;
  transform: skewX(-20deg) translateX(-50%);
  box-shadow: 5px 0px 0px #000;
}

.p5-esc-menu-image {
  position: absolute;
  top: 0; right: 0;
  width: 40vw; height: 100vh;
  background-color: #000;
  border-left: 10px solid #fff;
  transform: translateX(100%);
  transition: transform 0.5s cubic-bezier(0.19, 1, 0.22, 1) 0.1s;
  overflow: hidden;
}

.p5-esc-menu-overlay.active .p5-esc-menu-image {
  transform: translateX(0);
}

.menu-display-img {
  width: 100%; height: 100%;
  object-fit: cover;
  transform: scale(1.05);
}

.p5-esc-menu-items {
  position: absolute;
  top: 50%; left: 5%;
  transform: translateY(-50%);
  z-index: 201;
  opacity: 0;
  transition: opacity 0.3s ease 0.3s;
}

.p5-esc-menu-overlay.active .p5-esc-menu-items {
  opacity: 1;
}

.menu-item {
  display: flex;
  flex-direction: column;
  padding: 1.5rem 2rem;
  margin-bottom: 1rem;
  background-color: rgba(0, 0, 0, 0.7);
  border: 3px solid #fff;
  transform: skew(-5deg);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 8px 8px 0px #dc2626;
  min-width: 250px;
}

.menu-item:hover, .menu-item.active {
  background-color: #dc2626;
  transform: skew(-5deg) translateX(20px) scale(1.05);
  box-shadow: 12px 12px 0px #fff;
}

.menu-item-number {
  font-family: 'Impact', sans-serif;
  font-size: 2rem;
  color: #ffeb3b;
  line-height: 1;
}

.menu-item-title {
  font-family: 'Impact', sans-serif;
  font-size: 1.8rem;
  color: #fff;
  margin-top: 0.5rem;
}

.menu-item-subtitle {
  font-size: 0.9rem;
  color: #aaa;
  text-transform: uppercase;
  letter-spacing: 3px;
  margin-top: 0.3rem;
}

.p5-esc-hint {
  position: absolute;
  bottom: 3rem; left: 5%;
  z-index: 201;
  font-family: 'Impact', sans-serif;
  font-size: 1rem;
  color: #fff;
  opacity: 0;
  transition: opacity 0.3s ease 0.5s;
}

.p5-esc-menu-overlay.active .p5-esc-hint {
  opacity: 1;
}

.esc-key-hint {
  background-color: #dc2626;
  color: #fff;
  padding: 0.3rem 0.8rem;
  border: 2px solid #fff;
  margin-right: 0.5rem;
  transform: skew(-5deg);
  display: inline-block;
}

/* =======================================================
   P5 过渡动画
   ======================================================= */
.p5-transition-mask {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 100;
  pointer-events: none;
  visibility: hidden;
  display: flex;
  align-items: center;
}

.p5-transition-mask.active { visibility: visible; pointer-events: auto; }

.base-slice {
  position: absolute;
  width: 100vw; height: 50vh;
  z-index: 101;
  transition: transform 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}

.slice-red { top: 0; background-color: #dc2626; transform: translateY(-100%); }
.slice-black { bottom: 0; background-color: #000; transform: translateY(100%); }
.p5-transition-mask.active .slice-red { transform: translateY(0); }
.p5-transition-mask.active .slice-black { transform: translateY(0); }

.p5-perfect-card {
  position: relative;
  display: inline-block;
  max-width: 80vw; max-height: 75vh;
  background-color: #000;
  border: 8px solid #fff;
  box-shadow: 20px 20px 0px #dc2626, -10px -10px 0px #000;
  z-index: 105;
  overflow: hidden;
  opacity: 0;
  transition: transform 0.48s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s ease;
}

.p5-perfect-img {
  display: block;
  max-width: 100%; max-height: 70vh;
  object-fit: cover;
  transform: scale(1.05);
}

.p5-perfect-tape {
  position: absolute;
  bottom: -15px; left: 50%;
  transform: translateX(-50%) rotate(2deg);
  background-color: #ffeb3b; color: #000;
  padding: 0.3rem 2rem;
  font-family: 'Impact', sans-serif;
  font-weight: bold;
  font-size: 1.2rem;
  border: 3px solid #000;
  box-shadow: 5px 5px 0px #dc2626;
  z-index: 106;
  letter-spacing: 2px;
  white-space: nowrap;
}

/* Style 2 */
.p5-split-right-card {
  position: relative;
  display: inline-block;
  height: 100vh; max-width: 75vw;
  background-color: #000;
  border-left: 10px solid #fff;
  z-index: 105;
  overflow: hidden;
  opacity: 0;
  transform: translateX(110%);
  transition: transform 0.45s cubic-bezier(0.19, 1, 0.22, 1) 0.15s, opacity 0.3s ease 0.15s;
}

.p5-split-img { display: block; height: 100%; width: auto; min-width: 35vw; object-fit: cover; }
.p5-transition-mask.active.style-2 .p5-split-right-card { opacity: 1; transform: translateX(0) rotate(var(--card-rotate)) skewX(var(--card-skew)); }

.split-left-panel {
  position: absolute; top: 0; left: 0;
  width: 50vw; height: 100vh;
  background-color: #dc2626;
  border-right: 8px solid #000;
  clip-path: polygon(0 0, 100% 0, 40% 100%, 0% 100%);
  transform: translateX(-100%);
  z-index: 103;
  transition: transform 0.45s cubic-bezier(0.19, 1, 0.22, 1) 0.05s;
}
.p5-transition-mask.active.style-2 .split-left-panel { transform: translateX(0); }

.split-zigzag-line {
  position: absolute; top: 0; left: 38%;
  width: 45px; height: 100vh;
  background-color: #ffeb3b;
  transform: skewX(-20deg) scaleY(0);
  transform-origin: top;
  transition: transform 0.3s ease 0.35s;
  z-index: 104;
  box-shadow: 10px 0px 0px #000;
}
.p5-transition-mask.active.style-2 .split-zigzag-line { transform: skewX(-20deg) scaleY(1); }

/* Style 1 */
.style-1 .p5-perfect-card { transform: scale(0) rotate(-45deg); }
.p5-transition-mask.active.style-1 .p5-perfect-card { opacity: 1; transform: scale(1) rotate(var(--card-rotate)) skewX(var(--card-skew)); }

.eye-slash-back-red, .eye-slash-back-yellow {
  position: absolute; width: 100vw; height: 250px;
  z-index: 103;
  transform: skewY(-6deg) translateX(-100%);
  transition: transform 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}
.eye-slash-back-red { background-color: #dc2626; top: 40%; transition-delay: 0.05s; }
.eye-slash-back-yellow { background-color: #ffeb3b; top: 38%; transition-delay: 0s; }
.p5-transition-mask.active.style-1 .eye-slash-back-red,
.p5-transition-mask.active.style-1 .eye-slash-back-yellow { transform: skewY(-6deg) translateX(0); }

/* Style 3 */
.style-3 .p5-perfect-card { transform: translateY(115%) rotate(var(--card-rotate)) skewX(var(--card-skew)); transition: transform 0.58s cubic-bezier(0.34, 1.56, 0.64, 1) 0.12s, opacity 0.3s ease 0.12s; }
.p5-transition-mask.active.style-3 .p5-perfect-card { opacity: 1; transform: translateY(0) rotate(var(--card-rotate)) skewX(var(--card-skew)); }

.op-layer-red-bg {
  position: absolute; bottom: -5vh; left: -5vw;
  width: 110vw; height: 70vh;
  background-color: #dc2626;
  transform: translateY(110%) skewY(-6deg);
  transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) 0.05s;
  z-index: 103;
}
.p5-transition-mask.active.style-3 .op-layer-red-bg { transform: translateY(0) skewY(-6deg); }

/* Style 4 */
.style-4 .p5-perfect-card { transform: scale(0) rotate(-60deg); }
.p5-transition-mask.active.style-4 .p5-perfect-card { opacity: 1; transform: scale(1) rotate(var(--card-rotate)) skewX(var(--card-skew)); }

.shatter-shard-star { position: absolute; background-color: #dc2626; z-index: 103; transition: transform 0.45s cubic-bezier(0.19, 1, 0.22, 1); }
.shard-top-left { top: 0; left: 0; width: 50vw; height: 50vh; clip-path: polygon(0 0, 100% 0, 0 100%); transform: translate(-100%, -100%); }
.shard-bottom-right { bottom: 0; right: 0; width: 50vw; height: 50vh; background-color: #111; border-top: 4px solid #fff; clip-path: polygon(100% 0, 100% 100%, 0 100%); transform: translate(100%, 100%); transition-delay: 0.1s; }
.p5-transition-mask.active.style-4 .shard-top-left, .p5-transition-mask.active.style-4 .shard-bottom-right { transform: translate(0, 0); }

.p5-adaptive-container { position: relative; width: 100vw; height: 100vh; display: flex; align-items: center; z-index: 102; }
.align-left .p5-adaptive-container { justify-content: flex-start; padding-left: 10%; }
.align-right .p5-adaptive-container { justify-content: flex-end; padding-right: 0; }
.align-center .p5-adaptive-container { justify-content: center; }

.slice-text {
  position: absolute; bottom: 8%; right: 5%;
  font-family: 'Impact', sans-serif;
  font-size: 2.5rem;
  color: #ffeb3b;
  text-shadow: 4px 4px 0px #000;
  z-index: 104;
  transform: rotate(-5deg) scale(0);
  transition: transform 0.3s ease 0.4s;
  white-space: nowrap;
  background-color: #000;
  padding: 0.5rem 1.5rem;
  border: 3px solid #fff;
}
.p5-transition-mask.active .slice-text { transform: rotate(-5deg) scale(1); }

/* 弹窗 */
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
  width: 80%; max-width: 800px;
  padding: 3rem;
  position: relative;
  transform: scale(0.8) rotate(-5deg);
  box-shadow: 15px 15px 0px #dc2626;
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.2);
}
.p5-modal-overlay.active .p5-modal-card { transform: scale(1) rotate(-2deg); }

.close-btn {
  position: absolute; top: -15px; right: -15px;
  background-color: #dc2626; color: #fff;
  border: 3px solid #fff;
  font-family: 'Impact'; font-size: 1.5rem;
  width: 45px; height: 45px;
  cursor: pointer;
  box-shadow: 4px 4px 0px #000;
  transform: rotate(15deg);
}
.close-btn:hover { background-color: #fff; color: #000; transform: rotate(0deg) scale(1.1); }

.p5-modal-header { border-bottom: 4px solid #dc2626; padding-bottom: 1rem; margin-bottom: 1.5rem; }

.p5-badge {
  background-color: #ffeb3b; color: #000;
  padding: 0.3rem 0.8rem; font-weight: bold;
  display: inline-block; transform: skew(-10deg);
  margin-bottom: 0.5rem;
}

.p5-modal-header h2 { font-size: 2.5rem; }

.main-summary {
  font-size: 1.1rem; line-height: 1.6;
  margin-bottom: 2rem;
  background-color: #1a1a1a;
  padding: 1rem;
  border-left: 5px solid #dc2626;
}

.sub-nodes-container { margin-top: 1.5rem; }
.sub-section-title { font-family: 'Impact'; font-size: 1.2rem; color: #ffeb3b; margin-bottom: 1rem; }
.sub-nodes-list { display: flex; gap: 20px; }

.sub-node-box {
  flex: 1;
  background-color: #000;
  border: 2px solid #fff;
  padding: 1rem;
  transform: skew(-3deg);
  box-shadow: 5px 5px 0px #dc2626;
}

.sub-node-box h4 { color: #dc2626; font-size: 1.1rem; margin-bottom: 0.5rem; border-bottom: 1px dashed #fff; padding-bottom: 0.2rem; }
.sub-node-box p { font-size: 0.9rem; color: #ccc; line-height: 1.4; }
</style>
