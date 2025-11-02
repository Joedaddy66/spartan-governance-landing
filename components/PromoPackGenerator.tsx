
import React, { useState, useCallback } from 'react';
import { PromoPack } from '../types';
import { generatePromoPack } from '../services/geminiService';
import { LoadingSpinner } from './LoadingSpinner';
import { DownloadIcon, VideoIcon, ImageIcon, TextIcon, CalendarIcon, ErrorIcon } from './IconComponents';

export const PromoPackGenerator: React.FC = () => {
  const [topic, setTopic] = useState<string>('');
  const [useThinkingMode, setUseThinkingMode] = useState<boolean>(false);
  const [promoPack, setPromoPack] = useState<PromoPack | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = useCallback(async () => {
    if (!topic.trim()) {
      setError('Please enter a topic.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setPromoPack(null);

    try {
      const result = await generatePromoPack(topic, useThinkingMode);
      setPromoPack(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred.');
    } finally {
      setIsLoading(false);
    }
  }, [topic, useThinkingMode]);

  const handleDownloadCsv = () => {
    if (!promoPack) return;

    const headers = "Datetime_ISO,Platform,Post_Content,CTA_Link,Hashtags\n";
    const startDate = new Date();
    const rows = Array.from({ length: 14 }).flatMap((_, i) => {
      const day = new Date(startDate);
      day.setDate(startDate.getDate() + i);
      
      const postTime1 = new Date(day);
      postTime1.setHours(10, 30, 0, 0);

      const postTime2 = new Date(day);
      postTime2.setHours(19, 30, 0, 0);

      const sanitizedCaption = `"${promoPack.socialMediaCaption.replace(/"/g, '""')}"`;
      
      return [
        `${postTime1.toISOString()},Twitter,${sanitizedCaption},YOUR_SITE_LINK,#sidehustle #solocreator`,
        `${postTime2.toISOString()},Instagram,${sanitizedCaption},YOUR_SITE_LINK,#businesstips #entrepreneur`
      ];
    }).join('\n');

    const csvContent = headers + rows;
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    if (link.href) {
      URL.revokeObjectURL(link.href);
    }
    link.href = URL.createObjectURL(blob);
    link.download = `promo_schedule_${topic.toLowerCase().replace(/\s+/g, '_')}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <>
      <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-2xl shadow-lg border border-gray-700">
        <div className="flex flex-col sm:flex-row gap-4">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter your topic, e.g., 'How to find your first 5 clients'"
            className="flex-grow bg-gray-900 border border-gray-600 rounded-lg p-4 focus:ring-2 focus:ring-cyan-500 focus:outline-none transition duration-200"
            disabled={isLoading}
          />
          <button
            onClick={handleGenerate}
            disabled={isLoading || !topic.trim()}
            className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:from-cyan-600 hover:to-blue-700 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <LoadingSpinner />
                Generating...
              </>
            ) : (
              'Generate Promo Pack'
            )}
          </button>
        </div>
        <div className="mt-4 flex items-center">
            <label className="flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={useThinkingMode}
                onChange={(e) => setUseThinkingMode(e.target.checked)}
                className="form-checkbox h-5 w-5 text-cyan-500 bg-gray-700 border-gray-600 rounded focus:ring-cyan-600"
                disabled={isLoading}
              />
              <span className="ml-2 text-gray-400">
                Enable Thinking Mode (for complex topics)
              </span>
            </label>
        </div>
        {error && (
          <div className="mt-4 bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-lg flex items-center gap-3">
            <ErrorIcon className="w-5 h-5"/>
            <span>{error}</span>
          </div>
        )}
      </div>

      {isLoading && (
        <div className="text-center p-12">
          <div className="inline-block">
            <LoadingSpinner />
          </div>
          <p className="mt-4 text-lg text-gray-400 animate-pulse">
            {useThinkingMode ? "Thinking deeply... this will take extra time." : "Building your promo pack..."}
          </p>
        </div>
      )}

      {promoPack && (
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6 animate-fade-in">
          <div className="md:col-span-2 bg-gray-800/50 p-6 rounded-2xl border border-gray-700">
             <h2 className="text-2xl font-semibold mb-4 flex items-center gap-3 text-cyan-400"><TextIcon />Social Media Caption</h2>
             <p className="text-gray-300 whitespace-pre-wrap">{promoPack.socialMediaCaption}</p>
          </div>

          <div className="bg-gray-800/50 p-6 rounded-2xl border border-gray-700">
            <h2 className="text-2xl font-semibold mb-4 flex items-center gap-3 text-cyan-400"><VideoIcon />Video Scripts</h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-bold text-lg">15-Second Script</h3>
                <p className="text-gray-300 mt-1">{promoPack.videoScripts.fifteenSecond}</p>
              </div>
              <div className="border-t border-gray-700 my-4"></div>
              <div>
                <h3 className="font-bold text-lg">30-Second Script</h3>
                <p className="text-gray-300 mt-1">{promoPack.videoScripts.thirtySecond}</p>
              </div>
            </div>
          </div>

          <div className="bg-gray-800/50 p-6 rounded-2xl border border-gray-700">
            <h2 className="text-2xl font-semibold mb-4 flex items-center gap-3 text-cyan-400"><ImageIcon />Thumbnail Ideas</h2>
            <ul className="list-disc list-inside space-y-2 text-gray-300">
              {promoPack.thumbnailIdeas.map((idea, index) => (
                <li key={index}>{idea}</li>
              ))}
            </ul>
          </div>
          
          <div className="md:col-span-2 bg-gray-800/50 p-6 rounded-2xl border border-gray-700 flex flex-col sm:flex-row justify-between items-center gap-4">
            <div>
              <h2 className="text-2xl font-semibold flex items-center gap-3 text-cyan-400"><CalendarIcon />Posting Schedule</h2>
              <p className="text-gray-400 mt-1">A ready-to-use 14-day schedule for Twitter and Instagram.</p>
            </div>
            <button
              onClick={handleDownloadCsv}
              className="bg-gray-700 text-white font-bold py-3 px-6 rounded-lg hover:bg-gray-600 transition duration-200 flex items-center gap-2 w-full sm:w-auto"
            >
              <DownloadIcon />
              Download .CSV
            </button>
          </div>
        </div>
      )}
    </>
  );
};
