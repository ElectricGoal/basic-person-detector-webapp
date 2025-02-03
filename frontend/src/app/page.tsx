"use client";

import { useState } from "react";

interface ResultData {
  count: number;
  image_url: string;
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [result, setResult] = useState<ResultData | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;
    setUploading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      console.log(process.env.NEXT_PUBLIC_BACKEND_URL);
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/upload`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        throw new Error("Upload failed");
      }
      const data: ResultData = await res.json();
      setResult(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred");
      }
    }
    setUploading(false);
  };

  return (
    <div className="flex flex-col min-h-screen font-sans">
      <div className="container mx-auto px-4">
        {/* <section className="bg-white rounded-lg shadow-md p-8 max-w-xl mx-auto"> */}
        <h2 className="text-2xl font-semibold text-center mb-6 text-gray-800">
          Upload an Image
        </h2>
        <form onSubmit={handleSubmit} className="flex flex-col items-center">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="mb-6 text-gray-500"
          />
          <button
            type="submit"
            disabled={uploading}
            className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 transition"
          >
            {uploading ? "Uploading..." : "Upload & Detect"}
          </button>
        </form>
        {error && (
          <p className="text-red-500 mt-4 text-center">Error: {error}</p>
        )}
        {result && (
          <div className="mt-6 flex flex-col items-center">
            <p className="text-lg font-medium text-gray-800">
              Detected Persons: {result.count}
            </p>
            <img
              src={`${process.env.NEXT_PUBLIC_BACKEND_URL}${result.image_url}`}
              alt="Detection result"
              className="mt-4 border-2 border-green-600 rounded"
            />
          </div>
        )}
        {/* </section> */}
      </div>
    </div>
  );
}
