import React, { useEffect, useState } from 'react';
import OfferCard from './components/OfferCard';
import CTA from './components/CTA';
import fetchOffer from './api/fetchOffer';

interface Offer {
  topic: string;
  name: string;
  description: string;
  price_cents: number;
  currency: string;
  created_at: string;
  stripe_product_id?: string | null;
  stripe_price_id?: string | null;
}

const App: React.FC = () => {
  const [offer, setOffer] = useState<Offer | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchOffer()
      .then((data) => {
        setOffer(data);
      })
      .catch((err) => {
        setError(err.message || 'Unknown error');
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="p-4 text-center">Loading...</div>;
  }
  if (error || !offer) {
    return (
      <div className="p-4 text-center text-red-600">
        Failed to load offer: {error || 'No offer available'}
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-4 space-y-6">
      <OfferCard offer={offer} />
      <CTA priceCents={offer.price_cents} currency={offer.currency} productId={offer.stripe_product_id} />
    </div>
  );
};

export default App;