import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    template: "%s · NEXUS OPS",
    default: "NEXUS OPS",
  },
  description: "Multi-tenant enterprise operations & AI platform.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      {/* suppressHydrationWarning: browser extensions (e.g. ColorZilla) inject
          attributes into <body> before hydration, which trips React's diff. */}
      <body className="flex min-h-full flex-col" suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
