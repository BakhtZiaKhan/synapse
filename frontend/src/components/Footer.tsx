import { Github, Heart } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-white/50 backdrop-blur-sm border-t border-gray-200/50 mt-20">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="flex items-center space-x-2 text-gray-600 mb-4 md:mb-0">
            <span>Made with</span>
            <Heart className="w-4 h-4 text-red-500 animate-pulse" />
            <span>using Next.js & Tailwind CSS</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <Github className="w-5 h-5" />
              <span className="text-sm">View Source</span>
            </a>
          </div>
        </div>
        
        <div className="text-center mt-4 text-sm text-gray-500">
          <p>© 2024 Synapse Meeting Assistant. Built with free and open-source tools.</p>
        </div>
      </div>
    </footer>
  );
} 