"use client";

import React, { useState, useRef, DragEvent, ChangeEvent, KeyboardEvent } from "react";
import { UploadCloud, File, AlertCircle, CheckCircle2, FileText, Music, Video, Image, Loader2, X } from "lucide-react";
import { api, ApiError } from "@/lib/api";
import { Document } from "@/types/document";

interface FileUploadProps {
  onUploadSuccess: (doc: Document) => void;
}

const ACCEPTED_EXTENSIONS = [".pdf", ".docx", ".pptx", ".png", ".jpg", ".jpeg", ".txt", ".mp3", ".wav", ".mp4"];
const MAX_FILE_SIZE_MB = 50;

export const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const getFileIcon = (fileName: string) => {
    const ext = fileName.split(".").pop()?.toLowerCase();
    if (["mp3", "wav"].includes(ext || "")) return <Music className="w-8 h-8 text-amber-500" aria-hidden="true" />;
    if (["mp4"].includes(ext || "")) return <Video className="w-8 h-8 text-purple-500" aria-hidden="true" />;
    if (["png", "jpg", "jpeg"].includes(ext || "")) return <Image className="w-8 h-8 text-emerald-500" aria-hidden="true" />;
    if (["pdf", "docx", "pptx", "txt"].includes(ext || "")) return <FileText className="w-8 h-8 text-indigo-500" aria-hidden="true" />;
    return <File className="w-8 h-8 text-slate-500" aria-hidden="true" />;
  };

  const validateFile = (file: File): boolean => {
    setError(null);
    setSuccess(null);

    const ext = `.${file.name.split(".").pop()?.toLowerCase()}`;
    if (!ACCEPTED_EXTENSIONS.includes(ext)) {
      setError(`File type "${ext}" is not supported. Please upload one of: ${ACCEPTED_EXTENSIONS.join(", ")}`);
      return false;
    }

    if (file.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
      setError(`File size exceeds maximum allowable limit of ${MAX_FILE_SIZE_MB}MB.`);
      return false;
    }

    if (file.size === 0) {
      setError("The selected file is empty. Please select a valid document.");
      return false;
    }

    return true;
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && validateFile(file)) {
      setSelectedFile(file);
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file && validateFile(file)) {
      setSelectedFile(file);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      fileInputRef.current?.click();
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setError(null);
    setSuccess(null);

    try {
      const doc = await api.documents.upload(selectedFile);
      setSuccess(`Document "${doc.original_filename}" uploaded successfully. Foundation job initialized.`);
      setSelectedFile(null);
      if (fileInputRef.current) fileInputRef.current.value = "";
      onUploadSuccess(doc);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("Failed to upload document. Please check your network connection and try again.");
      }
    } finally {
      setUploading(false);
    }
  };

  const clearSelection = () => {
    setSelectedFile(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="w-full">
      {/* Hidden File Input */}
      <input
        ref={fileInputRef}
        id="document-upload-input"
        type="file"
        accept={ACCEPTED_EXTENSIONS.join(",")}
        onChange={handleFileChange}
        className="sr-only"
        aria-label="Upload educational material document"
      />

      {/* Accessible Drop Area */}
      <div
        role="button"
        tabIndex={0}
        onClick={() => fileInputRef.current?.click()}
        onKeyDown={handleKeyDown}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        aria-describedby="upload-instructions"
        className={`relative border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center transition-all cursor-pointer focus:outline-none focus-visible:ring-4 focus-visible:ring-indigo-500/50 ${
          dragOver
            ? "border-indigo-600 bg-indigo-50/50 dark:bg-indigo-950/40 scale-[1.01]"
            : "border-slate-300 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-900/40 hover:border-indigo-500 hover:bg-slate-50 dark:hover:bg-slate-800/40"
        }`}
      >
        <div className="flex flex-col items-center justify-center">
          <div className="w-14 h-14 rounded-2xl bg-indigo-100 dark:bg-indigo-900/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center mb-4 shadow-sm">
            <UploadCloud className="w-8 h-8" aria-hidden="true" />
          </div>

          <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-1">
            Upload Educational Document
          </h3>
          <p id="upload-instructions" className="text-sm text-slate-700 dark:text-slate-200 mb-4 max-w-md">
            Drag and drop your syllabus, slides, textbook chapter, worksheet, or audio/video lecture here, or{" "}
            <span className="text-indigo-600 dark:text-indigo-400 font-semibold underline underline-offset-2">
              browse files
            </span>
            .
          </p>

          {/* Formats and Limit badges */}
          <div className="flex flex-wrap items-center justify-center gap-1.5 max-w-xl text-xs text-slate-700 dark:text-slate-200">
            <span className="font-semibold text-slate-800 dark:text-slate-200">Accepted formats:</span>
            {["PDF", "DOCX", "PPTX", "PNG", "JPG", "TXT", "MP3", "WAV", "MP4"].map((fmt) => (
              <span
                key={fmt}
                className="px-2 py-0.5 rounded-md bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 font-mono text-[11px]"
              >
                {fmt}
              </span>
            ))}
            <span className="ml-2 px-2 py-0.5 rounded-md bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 font-medium">
              Max {MAX_FILE_SIZE_MB}MB
            </span>
          </div>
        </div>
      </div>

      {/* Selected File Card */}
      {selectedFile && (
        <div className="mt-5 p-4 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm flex items-center justify-between">
          <div className="flex items-center gap-3.5 min-w-0">
            {getFileIcon(selectedFile.name)}
            <div className="min-w-0">
              <p className="text-sm font-bold text-slate-900 dark:text-white truncate">
                {selectedFile.name}
              </p>
              <p className="text-xs text-slate-700 dark:text-slate-200">
                {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB • {selectedFile.type || "Document"}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={clearSelection}
              disabled={uploading}
              className="p-1.5 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 focus-visible:ring-2 focus-visible:ring-slate-400"
              aria-label="Remove selected file"
            >
              <X className="w-5 h-5" aria-hidden="true" />
            </button>
            <button
              onClick={handleUpload}
              disabled={uploading}
              className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-lg text-sm font-semibold shadow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-indigo-600"
            >
              {uploading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
                  <span>Uploading...</span>
                </>
              ) : (
                <span>Upload & Start Pipeline</span>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Feedback Alerts */}
      {error && (
        <div
          role="alert"
          className="mt-4 p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-200 flex items-start gap-3 text-sm"
        >
          <AlertCircle className="w-5 h-5 text-rose-600 dark:text-rose-400 shrink-0 mt-0.5" aria-hidden="true" />
          <div>
            <p className="font-semibold">Upload Error</p>
            <p>{error}</p>
          </div>
        </div>
      )}

      {success && (
        <div
          role="status"
          className="mt-4 p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200 flex items-start gap-3 text-sm"
        >
          <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" aria-hidden="true" />
          <div>
            <p className="font-semibold">Success</p>
            <p>{success}</p>
          </div>
        </div>
      )}
    </div>
  );
};
