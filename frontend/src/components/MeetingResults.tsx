'use client';

import { useState } from 'react';
import { CheckCircle, FileText, List, MessageSquare, Copy, Download, Sparkles } from 'lucide-react';

interface MeetingResultsProps {
  results: {
    title: string;
    transcript: string;
    summary: string;
    action_items: string[];
    key_decisions: string[];
    created_at: string;
  };
}

export default function MeetingResults({ results }: MeetingResultsProps) {
  const [activeTab, setActiveTab] = useState<'summary' | 'transcript' | 'actions' | 'decisions'>('summary');
  const [copied, setCopied] = useState<string | null>(null);

  const copyToClipboard = async (text: string, type: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(type);
      setTimeout(() => setCopied(null), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const downloadTranscript = () => {
    const blob = new Blob([results.transcript], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${results.title || 'meeting'}-transcript.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const tabs = [
    { id: 'summary', label: 'Summary', icon: MessageSquare },
    { id: 'transcript', label: 'Transcript', icon: FileText },
    { id: 'actions', label: 'Action Items', icon: List },
    { id: 'decisions', label: 'Key Decisions', icon: CheckCircle },
  ] as const;

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl border border-white/20 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-purple-700 px-8 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">{results.title}</h2>
            <p className="text-blue-100 text-sm flex items-center">
              <Sparkles className="w-4 h-4 mr-2" />
              Processed on {formatDate(results.created_at)}
            </p>
          </div>
          <button
            onClick={downloadTranscript}
            className="flex items-center space-x-2 px-4 py-2 bg-white/20 hover:bg-white/30 rounded-xl text-white transition-all duration-200 hover:scale-105"
          >
            <Download className="w-4 h-4" />
            <span className="text-sm font-medium">Download</span>
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 bg-gray-50/50">
        <nav className="flex space-x-8 px-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-all duration-200
                  ${activeTab === tab.id
                    ? 'border-blue-500 text-blue-600 bg-blue-50/50'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Content */}
      <div className="p-8">
        {activeTab === 'summary' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold text-gray-900 flex items-center">
                <MessageSquare className="w-5 h-5 mr-2 text-blue-600" />
                Meeting Summary
              </h3>
              <button
                onClick={() => copyToClipboard(results.summary, 'summary')}
                className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-600 hover:text-gray-800 transition-all duration-200 hover:bg-gray-100 rounded-lg"
              >
                <Copy className="w-4 h-4" />
                <span>{copied === 'summary' ? 'Copied!' : 'Copy'}</span>
              </button>
            </div>
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-6 border border-blue-100">
              <p className="text-gray-700 leading-relaxed text-lg">{results.summary}</p>
            </div>
          </div>
        )}

        {activeTab === 'transcript' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold text-gray-900 flex items-center">
                <FileText className="w-5 h-5 mr-2 text-purple-600" />
                Full Transcript
              </h3>
              <button
                onClick={() => copyToClipboard(results.transcript, 'transcript')}
                className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-600 hover:text-gray-800 transition-all duration-200 hover:bg-gray-100 rounded-lg"
              >
                <Copy className="w-4 h-4" />
                <span>{copied === 'transcript' ? 'Copied!' : 'Copy'}</span>
              </button>
            </div>
            <div className="bg-gradient-to-r from-gray-50 to-slate-50 rounded-2xl p-6 border border-gray-200 max-h-96 overflow-y-auto">
              <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{results.transcript}</p>
            </div>
          </div>
        )}

        {activeTab === 'actions' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold text-gray-900 flex items-center">
                <List className="w-5 h-5 mr-2 text-green-600" />
                Action Items
              </h3>
              <button
                onClick={() => copyToClipboard(results.action_items.join('\n'), 'actions')}
                className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-600 hover:text-gray-800 transition-all duration-200 hover:bg-gray-100 rounded-lg"
              >
                <Copy className="w-4 h-4" />
                <span>{copied === 'actions' ? 'Copied!' : 'Copy'}</span>
              </button>
            </div>
            {results.action_items.length > 0 ? (
              <div className="space-y-4">
                {results.action_items.map((item, index) => (
                  <div key={index} className="flex items-start space-x-4 p-6 bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl border border-green-200 shadow-sm hover:shadow-md transition-shadow duration-200">
                    <div className="bg-gradient-to-r from-green-500 to-emerald-500 w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <CheckCircle className="w-4 h-4 text-white" />
                    </div>
                    <p className="text-gray-700 text-lg leading-relaxed">{item}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <List className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                <p className="text-lg">No action items identified in this meeting.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'decisions' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold text-gray-900 flex items-center">
                <CheckCircle className="w-5 h-5 mr-2 text-blue-600" />
                Key Decisions
              </h3>
              <button
                onClick={() => copyToClipboard(results.key_decisions.join('\n'), 'decisions')}
                className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-600 hover:text-gray-800 transition-all duration-200 hover:bg-gray-100 rounded-lg"
              >
                <Copy className="w-4 h-4" />
                <span>{copied === 'decisions' ? 'Copied!' : 'Copy'}</span>
              </button>
            </div>
            {results.key_decisions.length > 0 ? (
              <div className="space-y-4">
                {results.key_decisions.map((decision, index) => (
                  <div key={index} className="flex items-start space-x-4 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl border border-blue-200 shadow-sm hover:shadow-md transition-shadow duration-200">
                    <div className="bg-gradient-to-r from-blue-500 to-indigo-500 w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <MessageSquare className="w-4 h-4 text-white" />
                    </div>
                    <p className="text-gray-700 text-lg leading-relaxed">{decision}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <MessageSquare className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                <p className="text-lg">No key decisions identified in this meeting.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
} 