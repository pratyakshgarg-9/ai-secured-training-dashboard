// --------------------
// DEVICE FINGERPRINT
// --------------------
function fingerprint() {
  return {
    user_agent: navigator.userAgent,
    platform: navigator.platform,
    vendor: navigator.vendor,
    hardware_concurrency: navigator.hardwareConcurrency,
    device_memory: navigator.deviceMemory || 0,
    screen: `${screen.width}x${screen.height}x${screen.colorDepth}`,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
  };
}

// --------------------
// LOCATION (DEMO SAFE)
// --------------------
function getLocation() {
  // Static location for demo & hackathon use
  // (Real systems use IP / GPS APIs)
  return {
    country: "IN",
    city: "Delhi",
    latitude: 28.6139,
    longitude: 77.2090
  };
}
