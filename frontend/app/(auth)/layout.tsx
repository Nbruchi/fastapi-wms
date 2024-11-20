import React, { ReactNode } from "react";
import Image from "next/image";

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <section className="hidden w-1/2 items-center justify-center bg-brand p-10 lg:flex xl:w-2/5">
        <div className="flex max-h-[800px] max-w-[430px] flex-col justify-center space-y-12">
          <Image
            src="/assets/images/logo-full.png"
            alt="logo"
            width={400}
            height={100}
            className="h-auto"
          />
          <div className="space-y-5 text-white">
            <h1 className="h1">Manage your wastes & recycling the best way</h1>
            <p className="body-1">
              This is a place where you can track your wastes and recycling
              activities in real-time.
            </p>
          </div>
          <Image
            className="hover: transition-all hover:rotate-2 hover:scale-105"
            src="/assets/images/files.png"
            alt="Files"
            width={540}
            height={360}
          />
        </div>
      </section>
      <section className="flex flex-1 items-center bg-white p-4 py-10 lg:justify-center lg:p-10 lg:py-0">
        <div className="mb-16 lg:hidden">
          <Image
            src="/assets/icons/logo-full.svg"
            alt="logo"
            width={224}
            height={82}
            className="h-auto w-[200px] lg:w-[250px]"
          />
        </div>
        {children}
      </section>
    </div>
  );
}
