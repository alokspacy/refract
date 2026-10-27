'use client';

import React, { useState, useRef } from 'react';

interface VoiceRecorderProps {
  onRecorded?: (blob: Blob) => void;
}

export function VoiceRecorder({ onRecorded }: VoiceRecorderProps) {
  const [recording, setRecording] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        if (onRecorded) onRecorded(audioBlob);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setRecording(true);
      setSeconds(0);
      timerRef.current = setInterval(() => setSeconds((s) => s + 1), 1000);
    } catch {
      alert('Microphone access denied or unavailable.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  };

  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm flex items-center justify-between">
      <div className="flex items-center gap-3">
        <span
          className={`h-3.5 w-3.5 rounded-full ${
            recording ? 'bg-red-500 animate-pulse' : 'bg-muted-foreground'
          }`}
          aria-hidden="true"
        />
        <span className="text-sm font-medium">
          {recording ? `Recording: ${seconds}s` : 'Voice Recorder Ready'}
        </span>
      </div>

      <button
        type="button"
        onClick={recording ? stopRecording : startRecording}
        className={`px-4 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition ${
          recording
            ? 'bg-red-600 text-white hover:bg-red-700'
            : 'bg-primary text-primary-foreground hover:opacity-90'
        }`}
      >
        {recording ? 'Stop Recording' : 'Record Audio'}
      </button>
    </div>
  );
}
