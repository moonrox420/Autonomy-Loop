import React, { useState } from 'react';

interface CTAProps {
  priceCents: number;
  currency: string;
  productId?: string | null;
}

const CTA: React.FC<CTAProps> = ({ priceCents, currency, productId }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const price = (priceCents / 100).toFixed(2);

  const handleCheckout = async () => {
    setLoading(true);
    setError(null);
    try {
      const base = import.meta.env.VITE_API_BASE_URL || 'http://localhost:9333';
      const res = await fetch(`${base}/checkout-session`, { method: 'POST' });
      if (!res.ok) {
        throw new Error(`Checkout failed (HTTP ${res.status})`);
      }
      const data = await res.json();
      window.location.href = data.url;
    } catch (err: any) {
      setError(err.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center space-y-2">
      <button
        onClick={handleCheckout}
        disabled={!productId || loading}
        className={`px-6 py-3 rounded-xl text-white font-medium transition-colors duration-200
        ${!productId || loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-primary hover:bg-primary-dark'}`}
      >
        {loading ? 'Processing...' : `Buy now for ${currency.toUpperCase()} ${price}`}
      </button>
      {!productId && (
        <p className="text-xs text-gray-500">Checkout not available for this offer.</p>
      )}
      {error && <p className="text-xs text-red-600">{error}</p>}
    </div>
  );
};

export default CTA;