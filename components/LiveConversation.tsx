import React, { useState, useRef, useEffect } from 'react';
import { GoogleGenAI, Modality, LiveSession, LiveServerMessage, Blob } from '@google/genai';
import { TranscriptionEntry } from '../types';
import { encode, decode, decodeAudioData } from '../utils/audioUtils';
import { MicrophoneIcon, StopIcon, ErrorIcon } from './IconComponents';

enum ConnectionState {
  DISCONNECTED,
  CONNECTING,
  CONNECTED,
  ERROR,
}

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY! });

export const LiveConversation: React.FC = () => {
  const [connectionState, setConnectionState] = useState(ConnectionState.DISCONNECTED);
  const [transcription, setTranscription] = useState<TranscriptionEntry[]>([]);
  const [error, setError] = useState<string | null>(null);

  const sessionPromiseRef = useRef<Promise<LiveSession> | null>(null);
  const inputAudioContextRef = useRef<AudioContext | null>(null);
  const outputAudioContextRef = useRef<AudioContext | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const scriptProcessorRef = useRef<ScriptProcessorNode | null>(null);
  
  const sources = useRef(new Set<AudioBufferSourceNode>()).current;
  const nextStartTime = useRef(0);
  
  const currentInputTranscription = useRef('');
  const currentOutputTranscription = useRef('');

  useEffect(() => {
    return () => {
      // Cleanup on unmount
      if (connectionState === ConnectionState.CONNECTED) {
        handleStop();
      }
    };
  }, [connectionState]);


  const handleStart = async () => {
    setConnectionState(ConnectionState.CONNECTING);
    setError(null);
    setTranscription([]);
    currentInputTranscription.current = '';
    currentOutputTranscription.current = '';

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStreamRef.current = stream;

      // Fix: Cast window to any to access webkitAudioContext for broader browser compatibility, resolving TypeScript errors.
      inputAudioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 16000 });
      outputAudioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });

      sessionPromiseRef.current = ai.live.connect({
        model: 'gemini-2.5-flash-native-audio-preview-09-2025',
        config: {
          responseModalities: [Modality.AUDIO],
          inputAudioTranscription: {},
          outputAudioTranscription: {},
          speechConfig: {
            voiceConfig: { prebuiltVoiceConfig: { voiceName: 'Zephyr' } },
          },
          systemInstruction: 'You are a friendly and helpful creative assistant. Keep your responses concise and conversational.'
        },
        callbacks: {
          onopen: () => {
            setConnectionState(ConnectionState.CONNECTED);
            const source = inputAudioContextRef.current!.createMediaStreamSource(mediaStreamRef.current!);
            const scriptProcessor = inputAudioContextRef.current!.createScriptProcessor(4096, 1, 1);
            scriptProcessorRef.current = scriptProcessor;

            scriptProcessor.onaudioprocess = (audioProcessingEvent) => {
              const inputData = audioProcessingEvent.inputBuffer.getChannelData(0);
              const pcmBlob = createBlob(inputData);
              sessionPromiseRef.current?.then((session) => {
                session.sendRealtimeInput({ media: pcmBlob });
              });
            };

            source.connect(scriptProcessor);
            scriptProcessor.connect(inputAudioContextRef.current!.destination);
          },
          onmessage: async (message: LiveServerMessage) => {
             if (message.serverContent?.inputTranscription) {
                currentInputTranscription.current += message.serverContent.inputTranscription.text;
             }
             if (message.serverContent?.outputTranscription) {
                currentOutputTranscription.current += message.serverContent.outputTranscription.text;
             }

             if (message.serverContent?.turnComplete) {
                const finalInput = currentInputTranscription.current.trim();
                const finalOutput = currentOutputTranscription.current.trim();

                setTranscription(prev => {
                    const newEntries: TranscriptionEntry[] = [];
                    if (finalInput) newEntries.push({ speaker: 'user', text: finalInput });
                    if (finalOutput) newEntries.push({ speaker: 'model', text: finalOutput });
                    return [...prev, ...newEntries];
                });

                currentInputTranscription.current = '';
                currentOutputTranscription.current = '';
             }

             const base64Audio = message.serverContent?.modelTurn?.parts[0]?.inlineData?.data;
             if (base64Audio && outputAudioContextRef.current) {
                nextStartTime.current = Math.max(nextStartTime.current, outputAudioContextRef.current.currentTime);
                const audioBuffer = await decodeAudioData(decode(base64Audio), outputAudioContextRef.current, 24000, 1);
                const source = outputAudioContextRef.current.createBufferSource();
                source.buffer = audioBuffer;
                source.connect(outputAudioContextRef.current.destination);
                source.addEventListener('ended', () => {
                  sources.delete(source);
                });
                source.start(nextStartTime.current);
                nextStartTime.current += audioBuffer.duration;
                sources.add(source);
             }

             if (message.serverContent?.interrupted) {
                sources.forEach(source => source.stop());
                sources.clear();
                nextStartTime.current = 0;
             }
          },
          onerror: (e: ErrorEvent) => {
            setError('An error occurred during the session. Please try again.');
            setConnectionState(ConnectionState.ERROR);
            console.error(e);
            handleStop();
          },
          onclose: (e: CloseEvent) => {
            handleStop();
          },
        },
      });
    } catch (err) {
        setError('Failed to get microphone permissions. Please allow microphone access and try again.');
        setConnectionState(ConnectionState.ERROR);
        console.error(err);
    }
  };
  
  const createBlob = (data: Float32Array): Blob => {
      const l = data.length;
      const int16 = new Int16Array(l);
      for (let i = 0; i < l; i++) {
        int16[i] = data[i] * 32768;
      }
      return {
        data: encode(new Uint8Array(int16.buffer)),
        mimeType: 'audio/pcm;rate=16000',
      };
  }

  const handleStop = () => {
    setConnectionState(ConnectionState.DISCONNECTED);
    
    mediaStreamRef.current?.getTracks().forEach(track => track.stop());
    scriptProcessorRef.current?.disconnect();
    inputAudioContextRef.current?.close();
    outputAudioContextRef.current?.close();

    sources.forEach(source => source.stop());
    sources.clear();
    nextStartTime.current = 0;
    
    sessionPromiseRef.current?.then(session => session.close());
    sessionPromiseRef.current = null;
  };

  const getButtonState = () => {
    switch(connectionState) {
        case ConnectionState.DISCONNECTED:
        case ConnectionState.ERROR:
            return <button onClick={handleStart} className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold py-4 px-8 rounded-full shadow-lg hover:scale-105 transition transform duration-200 flex items-center gap-3"><MicrophoneIcon/> Start Conversation</button>;
        case ConnectionState.CONNECTING:
            return <button disabled className="bg-gray-600 text-white font-bold py-4 px-8 rounded-full shadow-lg flex items-center gap-3 opacity-70 cursor-not-allowed">Connecting...</button>;
        case ConnectionState.CONNECTED:
            return <button onClick={handleStop} className="bg-red-600 text-white font-bold py-4 px-8 rounded-full shadow-lg hover:bg-red-700 transition duration-200 flex items-center gap-3"><StopIcon/> Stop Conversation</button>;
    }
  }
  
  return (
    <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-2xl shadow-lg border border-gray-700">
        <div className="flex flex-col items-center justify-center min-h-[400px]">
            {transcription.length === 0 && connectionState !== ConnectionState.CONNECTED && (
                <div className="text-center text-gray-400">
                    <MicrophoneIcon className="w-16 h-16 mx-auto mb-4"/>
                    <h2 className="text-2xl font-semibold text-gray-200">Ready to Talk</h2>
                    <p>Press "Start Conversation" to begin speaking with Gemini.</p>
                </div>
            )}
            <div className="w-full space-y-4 max-h-[400px] overflow-y-auto pr-2">
                {transcription.map((entry, index) => (
                    <div key={index} className={`p-3 rounded-lg ${entry.speaker === 'user' ? 'bg-blue-900/50 text-right' : 'bg-gray-700/50 text-left'}`}>
                        <p className="font-bold capitalize text-cyan-400">{entry.speaker}</p>
                        <p>{entry.text}</p>
                    </div>
                ))}
            </div>

        </div>
       <div className="mt-6 pt-4 border-t border-gray-700 flex flex-col items-center">
         {getButtonState()}
         {error && (
              <div className="mt-4 bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-lg flex items-center gap-3 w-full">
                <ErrorIcon className="w-5 h-5"/>
                <span>{error}</span>
              </div>
         )}
       </div>
    </div>
  );
};