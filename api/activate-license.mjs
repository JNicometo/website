import { kv } from "@vercel/kv";

export default async function handler(req, res) {
  if (req.method === "OPTIONS") {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).send("Method not allowed");
  }

  const { licenseKey, machineId } = req.body || {};

  if (!licenseKey || typeof licenseKey !== "string") {
    return res.status(400).json({ error: "Missing or invalid licenseKey" });
  }
  if (!machineId || typeof machineId !== "string") {
    return res.status(400).json({ error: "Missing or invalid machineId" });
  }

  const normalizedKey = licenseKey.trim().toUpperCase();

  const keyPattern = /^OWNIV-[A-Z2-9]{5}-[A-Z2-9]{5}-[A-Z2-9]{5}-[A-Z2-9]{5}$/;
  if (!keyPattern.test(normalizedKey)) {
    return res.status(400).json({ error: "Invalid license key format" });
  }

  const licenseData = await kv.get(normalizedKey);

  if (!licenseData) {
    return res.status(404).json({ error: "License key not found", code: "KEY_NOT_FOUND" });
  }

  if (!licenseData.activated) {
    licenseData.machineId = machineId;
    licenseData.activated = true;
    licenseData.activatedAt = new Date().toISOString();
    await kv.set(normalizedKey, licenseData);
    return res.json({ success: true, message: "License activated successfully", email: licenseData.email });
  }

  if (licenseData.machineId === machineId) {
    return res.json({ success: true, message: "License already activated on this machine", email: licenseData.email, reactivation: true });
  }

  return res.status(403).json({
    error: "License already activated on a different machine",
    code: "MACHINE_MISMATCH",
    hint: "Contact support at jnicometo@gritsoftware.dev for assistance",
  });
}
