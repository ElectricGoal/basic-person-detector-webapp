"use client";

import { useState, useEffect } from "react";

interface ResultItem {
  id: number;
  timestamp: string;
  count: number;
  image_url: string;
}

export default function Results() {
  const [results, setResults] = useState<ResultItem[]>([]);
  const [error, setError] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [modalImage, setModalImage] = useState<string | null>(null);
  const resultsPerPage = 10;

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/results`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch detection results");
        }
        return res.json();
      })
      .then((data: ResultItem[]) => setResults(data))
      .catch((err: unknown) => {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unknown error occurred");
        }
      });
  }, []);

  // Calculate pagination
  const indexOfLast = currentPage * resultsPerPage;
  const indexOfFirst = indexOfLast - resultsPerPage;
  const currentResults = results.slice(indexOfFirst, indexOfLast);
  const totalPages = Math.ceil(results.length / resultsPerPage);

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  return (
    <div className="flex flex-col min-h-screen font-sans">
        <div className="container mx-auto px-4">
          <h2 className="text-2xl font-semibold text-center mb-6 text-gray-800">
            Detection Results
          </h2>
          {error && <p className="text-red-500 text-center">Error: {error}</p>}
          {results.length === 0 ? (
            <p className="text-center text-gray-700">No results found.</p>
          ) : (
            <>
              <div className="overflow-x-auto">
                <table className="w-full bg-white rounded-lg shadow-md overflow-hidden">
                  <thead className="bg-green-600 text-white">
                    <tr>
                      <th className="py-2 px-4">ID</th>
                      <th className="py-2 px-4">Timestamp</th>
                      <th className="py-2 px-4">Count</th>
                      <th className="py-2 px-4">Image</th>
                      <th className="py-2 px-4">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {currentResults.map((result) => (
                      <tr key={result.id} className="text-center border-b text-gray-700">
                        <td className="py-2 px-4">{result.id}</td>
                        <td className="py-2 px-4">
                          {new Date(result.timestamp).toLocaleString()}
                        </td>
                        <td className="py-2 px-4">{result.count}</td>
                        <td className="py-2 px-4">
                          <img
                            src={`${process.env.NEXT_PUBLIC_BACKEND_URL}${result.image_url}`}
                            alt={`Detection ${result.id}`}
                            className="w-24 mx-auto cursor-pointer hover:opacity-75 transition text-gray-700 bg-green-600"
                            onClick={() =>
                              setModalImage(
                                `${process.env.NEXT_PUBLIC_BACKEND_URL}${result.image_url}`
                              )
                            }
                          />
                        </td>
                        <td className="py-2 px-4">
                          <DeleteButton
                            resultId={result.id}
                            onDeleted={() =>
                              setResults(
                                results.filter((r) => r.id !== result.id)
                              )
                            }
                          />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Pagination Controls */}
              <div className="flex justify-center mt-6 space-x-2">
                {Array.from({ length: totalPages }, (_, i) => (
                  <button
                    key={i + 1}
                    onClick={() => paginate(i + 1)}
                    className={`px-4 py-2 rounded ${
                      currentPage === i + 1
                        ? "bg-green-600 text-white"
                        : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                    }`}
                  >
                    {i + 1}
                  </button>
                ))}
              </div>
            </>
          )}

          {/* Modal for Full Image View */}
          {modalImage && (
            <div
              className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50"
              onClick={() => setModalImage(null)}
            >
              <div
                className="bg-white p-4 rounded-lg relative"
                onClick={(e) => e.stopPropagation()}
              >
                <img
                  src={modalImage}
                  alt="Full view"
                  className="max-w-full max-h-[80vh]"
                />
                <button
                  className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
                  onClick={() => setModalImage(null)}
                >
                  Close
                </button>
              </div>
            </div>
          )}
        </div>
    </div>
  );
}

interface DeleteButtonProps {
  resultId: number;
  onDeleted: () => void;
}

function DeleteButton({ resultId, onDeleted }: DeleteButtonProps) {
  const [error, setError] = useState("");

  const handleDelete = async () => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/results/${resultId}`,
        { method: "DELETE" }
      );
      if (res.status !== 204) {
        throw new Error("Failed to delete the record");
      }
      onDeleted();
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred");
      }
    }
  };

  return (
    <div className="flex flex-col items-center">
      <button
        onClick={handleDelete}
        className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 transition"
      >
        Delete
      </button>
      {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
    </div>
  );
}
