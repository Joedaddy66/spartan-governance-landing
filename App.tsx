
import React, { useState } from 'react';
import { PromoPackGenerator } from './components/PromoPackGenerator';
import { LiveConversation } from './components/LiveConversation';
import { Login } from './components/Login';
import { Signup } from './components/Signup';
import { RobotIcon } from './components/IconComponents';

type Tab = 'generator' | 'live';
type View = 'home' | 'login' | 'signup';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>('generator');
  const [currentView, setCurrentView] = useState<View>('home');

  const renderTabContent = () => {
    switch (activeTab) {
      case 'generator':
        return <PromoPackGenerator />;
      case 'live':
        return <LiveConversation />;
      default:
        return null;
    }
  };

  const TabButton: React.FC<{tabName: Tab, label: string}> = ({ tabName, label }) => (
     <button
        onClick={() => setActiveTab(tabName)}
        className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
          activeTab === tabName
            ? 'bg-cyan-500 text-white'
            : 'text-gray-400 hover:bg-gray-700 hover:text-white'
        }`}
      >
        {label}
      </button>
  );

  // Render login view
  if (currentView === 'login') {
    return (
      <div className="min-h-screen bg-gray-900 text-gray-200 flex flex-col items-center justify-center p-4 sm:p-6 lg:p-8">
        <Login
          onSwitchToSignup={() => setCurrentView('signup')}
          onBack={() => setCurrentView('home')}
        />
      </div>
    );
  }

  // Render signup view
  if (currentView === 'signup') {
    return (
      <div className="min-h-screen bg-gray-900 text-gray-200 flex flex-col items-center justify-center p-4 sm:p-6 lg:p-8">
        <Signup
          onSwitchToLogin={() => setCurrentView('login')}
          onBack={() => setCurrentView('home')}
        />
      </div>
    );
  }

  // Render home view
  return (
    <div className="min-h-screen bg-gray-900 text-gray-200 flex flex-col items-center p-4 sm:p-6 lg:p-8">
      <div className="w-full max-w-4xl mx-auto">
        <header className="text-center mb-8">
          <div className="flex items-center justify-center gap-4 mb-4">
            <RobotIcon className="w-12 h-12 text-cyan-400"/>
            <h1 className="text-4xl sm:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-500">
              AI Content Assistant
            </h1>
          </div>
          <p className="text-gray-400 text-lg mb-4">
            Generate marketing kits or have a live conversation with Gemini.
          </p>

          {/* Auth buttons */}
          <div className="flex justify-center gap-4 mb-4">
            <button
              onClick={() => setCurrentView('login')}
              className="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors border border-gray-600"
            >
              Login
            </button>
            <button
              onClick={() => setCurrentView('signup')}
              className="px-6 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 text-white rounded-lg font-medium transition-all shadow-lg shadow-cyan-500/20"
            >
              Sign Up for Services
            </button>
          </div>

          {/* Learn More button */}
          <div className="mt-4">
            <button
              onClick={() => setCurrentView('signup')}
              className="text-cyan-400 hover:text-cyan-300 font-medium underline underline-offset-4"
            >
              Learn More →
            </button>
          </div>
        </header>

        <div className="flex justify-center mb-6 bg-gray-800/50 p-1.5 rounded-lg border border-gray-700 w-fit mx-auto">
          <TabButton tabName="generator" label="Promo Pack Builder" />
          <TabButton tabName="live" label="Live Conversation" />
        </div>

        <main>
          {renderTabContent()}
        </main>
      </div>
    </div>
  );
};

export default App;