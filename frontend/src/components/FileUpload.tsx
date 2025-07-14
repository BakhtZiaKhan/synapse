'use client';

import { useState, useCallback } from 'react';
import { Upload, FileAudio, X, Sparkles } from 'lucide-react';

interface FileUploadProps {
  onUpload: (file: File, meetingTitle?: string) => void;
}

export default function FileUpload({ onUpload }: FileUploadProps) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [meetingTitle, setMeetingTitle] = useState('');

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      console.log('Dropped file:', file.name, 'Type:', file.type);
      if (isValidFile(file)) {
        setSelectedFile(file);
        console.log('File accepted');
      } else {
        console.log('File rejected - not a valid audio/video format');
      }
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      console.log('Selected file:', file.name, 'Type:', file.type);
      if (isValidFile(file)) {
        setSelectedFile(file);
        console.log('File accepted');
      } else {
        console.log('File rejected - not a valid audio/video format');
      }
    }
  };

  const isValidFile = (file: File): boolean => {
    // Check MIME type first
    const validMimeTypes = [
      'audio/mp3', 'audio/wav', 'audio/m4a', 'audio/aac',
      'audio/ogg', 'audio/flac', 'audio/wma', 'audio/aiff',
      'video/mp4', 'video/avi', 'video/mov', 'video/mkv',
      'video/wmv', 'video/flv', 'video/webm'
    ];
    
    // If MIME type is valid, accept it
    if (validMimeTypes.includes(file.type)) {
      return true;
    }
    
    // If MIME type is not recognized, check file extension
    const fileName = file.name.toLowerCase();
    const validExtensions = [
      '.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac', '.wma', '.aiff',
      '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'
    ];
    
    return validExtensions.some(ext => fileName.endsWith(ext));
  };

  const handleSubmit = () => {
    if (selectedFile) {
      onUpload(selectedFile, meetingTitle || undefined);
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
  };

  return (
    <div className="space-y-8">
      {/* File Upload Area */}
      <div
        className={`
          relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 group
          ${dragActive 
            ? 'border-blue-500 bg-blue-50/50 scale-105 shadow-lg' 
            : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50/30 hover:scale-[1.02]'
          }
        `}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept="audio/*,video/*"
          onChange={handleFileSelect}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        
        <div className="space-y-6">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full blur-lg opacity-20 group-hover:opacity-40 transition-opacity duration-300"></div>
            <div className="relative bg-gradient-to-r from-blue-500 to-purple-500 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto group-hover:scale-110 transition-transform duration-300">
              <Upload className="w-10 h-10 text-white" />
            </div>
          </div>
          <div>
            <p className="text-xl font-semibold text-gray-900 mb-2">
              Drop your audio or video file here
            </p>
            <p className="text-gray-500 text-lg">or click to browse</p>
            <div className="flex items-center justify-center mt-4 text-sm text-gray-400">
              <Sparkles className="w-4 h-4 mr-2" />
              <span>Supports all major audio and video formats</span>
            </div>
          </div>
        </div>
      </div>

      {/* Selected File */}
      {selectedFile && (
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-2xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-gradient-to-r from-green-500 to-emerald-500 w-12 h-12 rounded-xl flex items-center justify-center">
                <FileAudio className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="font-semibold text-green-900 text-lg">{selectedFile.name}</p>
                <p className="text-sm text-green-700">
                  {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                </p>
              </div>
            </div>
            <button
              onClick={removeFile}
              className="text-green-600 hover:text-green-800 p-2 rounded-lg hover:bg-green-100 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}

      {/* Meeting Title Input */}
      <div>
        <label htmlFor="meeting-title" className="block text-sm font-semibold text-gray-700 mb-3">
          Meeting Title (Optional)
        </label>
        <input
          type="text"
          id="meeting-title"
          value={meetingTitle}
          onChange={(e) => setMeetingTitle(e.target.value)}
          placeholder="e.g., Weekly Team Meeting, Project Review, Client Call"
          className="w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg transition-all duration-200 hover:border-gray-400"
        />
      </div>

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        disabled={!selectedFile}
        className={`
          w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all duration-300 transform
          ${selectedFile
            ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 hover:scale-[1.02] shadow-lg hover:shadow-xl focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }
        `}
      >
        {selectedFile ? (
          <div className="flex items-center justify-center space-x-2">
            <Sparkles className="w-5 h-5" />
            <span>Process Meeting</span>
          </div>
        ) : (
          'Select a file to continue'
        )}
      </button>
    </div>
  );
} 