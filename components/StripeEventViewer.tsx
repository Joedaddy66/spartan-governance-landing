interface Event {
  id: string;
  type: string;
  created: string;
  data: any;
}

export default function StripeEventViewer({ events }: { events: Event[] }) {
  return (
    <div>
      <h1>Stripe Events</h1>
      <ul>
        {events.map((event) => (
          <li key={event.id}>
            <strong>{event.type}</strong> — {new Date(event.created).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
}