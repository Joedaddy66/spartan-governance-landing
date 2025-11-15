import { Client } from 'pg';
import StripeEventViewer from '@/components/StripeEventViewer';

export default async function Page() {
  const client = new Client({
    connectionString: process.env.POSTGRES_URL,
  });

  await client.connect();

  const res = await client.query(
    'SELECT id, type, created, data FROM stripe_events ORDER BY created DESC LIMIT 20'
  );

  await client.end();

  const events = res.rows.map((event) => ({
    id: event.id,
    type: event.type,
    created: event.created.toISOString(),
    data: event.data,
  }));

  return <StripeEventViewer events={events} />;
}