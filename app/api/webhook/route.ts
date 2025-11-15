import Stripe from 'stripe';
import { buffer } from 'micro';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY as string);
export const config = { api: { bodyParser: false } };

export default async function handler(req: any, res: any) {
  const sig = req.headers['stripe-signature'];
  const buf = await buffer(req);

  let event;
  try {
    event = stripe.webhooks.constructEvent(buf, sig, process.env.STRIPE_WEBHOOK_SECRET as string);
  } catch (err: any) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Handle event types
  switch (event.type) {
    case 'checkout.session.completed':
      console.log('✅ Checkout completed:', event.data.object);
      break;
    case 'invoice.paid':
      console.log('💰 Invoice paid:', event.data.object);
      break;
    // Add more cases as needed
  }

  res.status(200).json({ received: true });
}