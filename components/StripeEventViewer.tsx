'use client';
import { useEffect, useState } from 'react';
import { getFirestore, collection, query, orderBy, limit, getDocs } from 'firebase/firestore';
import { initializeApp } from 'firebase/app';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export default function StripeEventViewer() {
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    const fetchEvents = async () => {
      const q = query(collection(db, 'stripe_events'), orderBy('receivedAt', 'desc'), limit(5));
      const snapshot = await getDocs(q);
      setEvents(snapshot.docs.map(doc => doc.data()));
    };
    fetchEvents();
  }, []);

  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="text-xl font-bold mb-2">Recent Stripe Events</h2>
      <ul>
        {events.map((event, idx) => (
          <li key={idx} className="mb-2 border-b pb-2">
            <strong>{event.type}</strong><br />
            <code>{JSON.stringify(event.data, null, 2)}</code>
          </li>
        ))}
      </ul>
    </div>
  );
}
