"use client";

import Image from "next/image";
import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";

import { convertFileToUrl } from "@/lib/utils";

type FileUploaderProps = {
  file: File | undefined;
  onChange: (files: File[]) => void;
};

const AvatarUploader = ({ file, onChange }: FileUploaderProps) => {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      onChange(acceptedFiles);
    },
    [onChange]
  );

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div {...getRootProps()} className="file-upload">
      <input {...getInputProps()} />
      {file ? (
        <Image
          src={convertFileToUrl(file)}
          width={1000}
          height={1000}
          alt="uploaded image"
          className="max-h-[200px] overflow-hidden object-cover"
        />
      ) : (
        <>
          <Image
            src="/assets/icons/upload.svg"
            width={40}
            height={40}
            alt="upload"
          />
        </>
      )}
    </div>
  );
};

export default AvatarUploader;
