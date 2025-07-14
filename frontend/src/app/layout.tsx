import './styles.css'

export const metadata = {
  title: 'Synapse - AI Meeting Assistant',
  description: 'Transform your meeting recordings into actionable insights with AI-powered transcription, summarization, and analysis.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
