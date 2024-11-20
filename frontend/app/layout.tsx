import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { ReactNode } from "react";

export const metadata: Metadata = {
    title: "Wms",
    description: "Waste Management System for all",
};

const poppins = localFont({
    src: [
        {
            path: "./fonts/Poppins-Black.ttf",
            weight: "900",
            style: "normal",
        },
        {
            path: "./fonts/Poppins-ExtraBold.ttf",
            weight: "800",
            style: "normal",
        },
        {
            path: "./fonts/Poppins-Bold.ttf",
            weight: "700",
            style: "normal",
        },
        {
            path: "./fonts/Poppins-SemiBold.ttf",
            weight: "600",
            style: "normal",
        },
        {
            path: "./fonts/Poppins-Medium.ttf",
            weight: "500",
            style: "normal",
        },
        {
            path: "./fonts/Poppins-Regular.ttf",
            weight: "400",
            style: "normal",
        },
        {
            path: "./fonts/Poppins-Thin.ttf",
            weight: "300",
            style: "normal",
        },
        {
            path: "./fonts/Poppins-Light.ttf",
            weight: "200",
            style: "normal",
        },
        {
            path: "./fonts/Poppins-ExtraLight.ttf",
            weight: "100",
            style: "normal",
        },
    ],
    variable: "--font-poppins",
});

export default function Layout({
    children,
}: Readonly<{
    children: ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={`${poppins.variable} font-poppins antialiased`}>
                {children}
            </body>
        </html>
    );
}
