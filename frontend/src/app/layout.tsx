// app/layout.tsx
import Link from "next/link";
import "./globals.css"; // Ensure Tailwind’s CSS is imported

export const metadata = {
  title: "Person detector",
  description: "Perwson detector Web App",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head />
      <body className="min-h-screen bg-white">
        <nav className="bg-green-600 shadow">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between items-center h-16">
              <div className="flex space-x-4">
                <Link
                  href="/"
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:bg-yellow-500"
                >
                  Home
                </Link>
                <Link
                  href="/results"
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:bg-yellow-500"
                >
                  Results
                </Link>
              </div>
            </div>
          </div>
        </nav>
        <main className="p-8">{children}</main>
        <footer className="bg-green-600 text-white py-4 text-center">
          &copy; {new Date().getFullYear()} Basic Person Detector Web App
        </footer>
      </body>
    </html>
  );
}
