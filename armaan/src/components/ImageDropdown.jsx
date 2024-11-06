import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import ParticlesComponent from './ParticlesComponent';


const ImageDropBox = () => {
    const onDrop = useCallback((acceptedFiles) => {
    // Handle the dropped files
    const file = acceptedFiles[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const imgSrc = e.target.result;
      console.log('Image file data: ', imgSrc);
      // Do something with the image source (e.g., display it, upload it, etc.)
    };
    reader.readAsDataURL(file);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: 'image/*', // Accept only image files
    multiple: false,   // Allow only one file at a time
  });

  return (
    <div
      {...getRootProps()}
      className={`border-4 border-double rounded-lg w-80 h-80 mt-20 p-20 flex justify-center items-center text-color-white font-sora font-bold tracking-tighter text-1xl md:auto text-slate-300
        ${isDragActive ? 'border-blue-500 bg-blue-100' : 'border-gray-100 bg-slate-950'}`}
    >
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop the Image Here ...</p>
      ) : (
        <p>Drag and Drop an Image, or Click to Select</p>
      )}
    </div>
  );
};

export default ImageDropBox;

