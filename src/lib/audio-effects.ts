/**
 * Sound effect feedback controller with volume attenuation for neurodivergent sensory comfort.
 */
class AudioFeedbackController {
  private volume: number = 0.5;
  private muted: boolean = false;

  setVolume(vol: number): void {
    this.volume = Math.max(0, Math.min(1, vol));
  }

  setMuted(muted: boolean): void {
    this.muted = muted;
  }

  playChime(): void {
    if (this.muted || typeof window === "undefined") return;
    try {
      const ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
      gain.gain.setValueAtTime(this.volume * 0.1, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.3);
    } catch {
      // AudioContext not allowed or unsupported
    }
  }
}

export const soundEffects = new AudioFeedbackController();
