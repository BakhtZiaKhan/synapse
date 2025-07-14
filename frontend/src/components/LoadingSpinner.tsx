import { Sparkles } from 'lucide-react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
}

export default function LoadingSpinner({ size = 'md', text }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
  };

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative">
        {/* Outer glow */}
        <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full blur-lg opacity-30 animate-pulse"></div>
        
        {/* Main spinner */}
        <div className={`relative ${sizeClasses[size]} border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin`}></div>
        
        {/* Inner sparkle */}
        <div className="absolute inset-0 flex items-center justify-center">
          <Sparkles className="w-4 h-4 text-blue-600 animate-bounce-gentle" />
        </div>
      </div>
      
      {text && (
        <p className="mt-4 text-gray-600 text-center font-medium">{text}</p>
      )}
    </div>
  );
} 