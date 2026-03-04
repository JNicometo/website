import { kv } from "@vercel/kv";

export default async function handler(req, res) {
  if (req.method === "OPTIONS") {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    return res.status(200).end();
  }

  if (req.method !== "GET") {
    return res.status(405).send("Method not allowed");
  }

  const sessionId = req.query.session_id;

  if (!sessionId || typeof sessionId !== "string" || !sessionId.startsWith("cs_")) {
    return res.status(400).json({ error: "Missing or invalid session_id" });
  }

  const licenseKey = await kv.get(`session_${sessionId}`);

  if (!licenseKey) {
    return res.status(404).json({
      error: "License not found for this session",
      hint: "This may take a few seconds. Please refresh the page.",
    });
  }

  const licenseData = await kv.get(licenseKey);

  return res.json({
    licenseKey,
    email: licenseData?.email || null,
    created: licenseData?.created || null,
  });
}
