import Stripe from "stripe";

export default async function handler(req, res) {
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }
  if (req.method !== "POST") {
    return res.status(405).send("Method not allowed");
  }

  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
  const domain = process.env.DOMAIN || "https://gritsoftware.dev";

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      line_items: [
        {
          price_data: {
            currency: "usd",
            product_data: {
              name: "OwnInvoice Desktop",
              description: "Professional desktop invoicing software - Lifetime license",
              images: [`${domain}/OwnInvoice_Banner-B_v2.png`],
            },
            unit_amount: 19900,
          },
          quantity: 1,
        },
      ],
      mode: "payment",
      success_url: `${domain}/success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${domain}/index.html#pricing`,
      allow_promotion_codes: true,
    });

    res.json({ url: session.url });
  } catch (error) {
    console.error("Stripe error:", error.message);
    res.status(500).json({ error: error.message });
  }
}
