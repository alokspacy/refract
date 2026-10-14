/**
 * Procedural ambient noise synthesizer (Brownian, Pink, and Soft White Noise)
 * designed for ADHD executive function and cognitive focus.
 */
class AmbientSoundGenerator {
  private audioCtx: AudioContext | null = null;
  private noiseNode: AudioNode | null = null;
  private gainNode: GainNode | null = null;
  private isPlaying: boolean = false;

  start(type: "brown" | "pink" | "white" = "brown", volume: number = 0.2): void {
    if (typeof window === "undefined") return;
    this.stop();

    const CtxClass = window.AudioContext || (window as any).webkitAudioContext;
    this.audioCtx = new CtxClass();
    const bufferSize = this.audioCtx.sampleRate * 2;
    const buffer = this.audioCtx.createBuffer(1, bufferSize, this.audioCtx.sampleRate);
    const data = buffer.getChannelData(0);

    let lastOut = 0.0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      if (type === "brown") {
        data[i] = (lastOut + 0.02 * white) / 1.02;
        lastOut = data[i];
        data[i] *= 3.5;
      } else {
        data[i] = white * 0.1;
      }
    }

    const whiteNoise = this.audioCtx.createBufferSource();
    whiteNoise.buffer = buffer;
    whiteNoise.loop = true;

    this.gainNode = this.audioCtx.createGain();
    this.gainNode.gain.setValueAtTime(volume, this.audioCtx.currentTime);

    whiteNoise.connect(this.gainNode);
    this.gainNode.connect(this.audioCtx.destination);
    whiteNoise.start();

    this.noiseNode = whiteNoise;
    this.isPlaying = true;
  }

  setVolume(vol: number): void {
    if (this.gainNode && this.audioCtx) {
      this.gainNode.gain.setValueAtTime(Math.max(0, Math.min(1, vol)), this.audioCtx.currentTime);
    }
  }

  stop(): void {
    if (this.noiseNode) {
      try { (this.noiseNode as any).stop(); } catch {}
      this.noiseNode = null;
    }
    if (this.audioCtx) {
      try { this.audioCtx.close(); } catch {}
      this.audioCtx = null;
    }
    this.isPlaying = false;
  }

  active(): boolean {
    return this.isPlaying;
  }
}

export const ambientSound = new AmbientSoundGenerator();
