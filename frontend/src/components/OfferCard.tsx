import React from 'react';

interface OfferCardProps {
  offer: {
    name: string;
    description: string;
    price_cents: number;
    currency: string;
    created_at: string;
  };
}

const OfferCard: React.FC<OfferCardProps> = ({ offer }) => {
  const price = (offer.price_cents / 100).toFixed(2);
  return (
    <div className="bg-white shadow-md rounded-xl p-6 space-y-3">
      <h2 className="text-2xl font-bold text-gray-800">{offer.name}</h2>
      <p className="text-gray-600">{offer.description}</p>
      <div className="text-xl font-semibold text-primary-dark">
        {offer.currency.toUpperCase()} {price}
      </div>
      <p className="text-xs text-gray-400">Generated on {new Date(offer.created_at).toLocaleString()}</p>
    </div>
  );
};

export default OfferCard;