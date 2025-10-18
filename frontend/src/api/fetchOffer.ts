/**
 * Fetch the latest offer from the backend API.
 *
 * The API base URL defaults to localhost:9333 but can be overridden by
 * defining VITE_API_BASE_URL in the environment. Returns the parsed JSON
 * object on success. Throws an Error if the request fails.
 */
export default async function fetchOffer() {
  const base = import.meta.env.VITE_API_BASE_URL || 'http://localhost:9333';
  const res = await fetch(`${base}/offers/latest`);
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  return await res.json();
}