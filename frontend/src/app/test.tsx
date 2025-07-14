export default function TestPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
      <div className="bg-white rounded-2xl p-8 shadow-2xl">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Tailwind Test</h1>
        <p className="text-gray-600">If you can see this styled text, Tailwind is working!</p>
        <div className="mt-4 p-4 bg-blue-100 rounded-lg">
          <p className="text-blue-800">This should have a blue background</p>
        </div>
      </div>
    </div>
  );
} 