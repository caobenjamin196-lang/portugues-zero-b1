/* PT-BR 发音：优先本地 edge-tts 神经语音 mp3，失败回退 Web Speech API。
 * 用法：TTS.speak(text, audioUrl?) ；TTS.wordAudioUrl(entry, week) ；TTS.conjAudioUrl(verb, personKey)
 * 文件名安全化规则必须与 tools/generate_audio.py 的 safe() 保持一致。 */
const TTS = (() => {
  const safeName = s => String(s == null ? '' : s)
    .trim().toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9à-ÿ_-]/g, '');

  const wordAudioUrl = (entry, week) =>
    `assets/audio/words/w${week}_${entry.rank}_${safeName(entry.pt)}.mp3`;

  /* personKey: eu / tu / ele / nos / eles */
  const conjAudioUrl = (verb, personKey) =>
    `assets/audio/conj/${safeName(verb)}_${personKey}.mp3`;

  /* 例句音频：与 words 同名规范，放在 examples/ 目录 */
  const exampleAudioUrl = (entry, week) =>
    `assets/audio/examples/w${week}_${entry.rank}_${safeName(entry.pt)}.mp3`;

  /* ===== Web Speech 回退 ===== */
  function ptVoice() {
    if (!('speechSynthesis' in window)) return null;
    const vs = speechSynthesis.getVoices();
    const norm = l => String(l || '').toLowerCase().replace('_', '-');
    // 优先高质量语音：Google / Microsoft / Apple 增强版 pt-BR
    const br = vs.filter(v => norm(v.lang).startsWith('pt-br'));
    return br.find(v => /google/i.test(v.name))
        || br.find(v => /microsoft|online|natural/i.test(v.name))
        || br.find(v => v.localService === false)
        || br[0]
        || vs.find(v => norm(v.lang).startsWith('pt'))
        || null;
  }

  function speakFallback(text) {
    if (!('speechSynthesis' in window)) { toast('⚠️ 音频不可用，且此浏览器不支持语音合成'); return; }
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'pt-BR';
    u.rate = 0.92;
    const v = ptVoice();
    if (v) u.voice = v;
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
  }

  if ('speechSynthesis' in window) {
    speechSynthesis.getVoices(); // 预热语音列表（iOS/Chrome 异步加载）
    speechSynthesis.onvoiceschanged = () => speechSynthesis.getVoices();
  }

  let current = null; // 当前播放的 Audio，避免重叠
  function speak(text, audioUrl) {
    if (!text) return;
    if (current) { try { current.pause(); } catch (e) {} current = null; }
    if (!audioUrl) { speakFallback(text); return; }
    try {
      const a = new Audio(audioUrl);
      current = a;
      let fellBack = false;
      const fallback = () => { if (!fellBack) { fellBack = true; speakFallback(text); } };
      a.onerror = fallback;
      a.play().catch(fallback);
    } catch (e) {
      speakFallback(text);
    }
  }

  return { safeName, wordAudioUrl, conjAudioUrl, exampleAudioUrl, speak, speakFallback };
})();
