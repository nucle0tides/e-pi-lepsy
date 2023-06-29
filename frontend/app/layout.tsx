import "./globals.css";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"], display: "swap" });

export const metadata = {
  title: "e-pi-lepsy",
  description: `latest and greatest iteration of managing, tracking, and visualizing my chronically ill dog's health`,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      {/* TODO: learn how NextJS's stupid ass font logic works */}
      <body className={inter.className}>
        <main className="flex min-h-screen w-full flex-col overflow-hidden">
          {children}
        </main>
      </body>
    </html>
  );
}
