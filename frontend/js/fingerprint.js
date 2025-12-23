function getFingerprint() {
  return {
    user_agent: navigator.userAgent,
    platform: navigator.userAgentData
      ? navigator.userAgentData.platform
      : "unknown",
    language: navigator.language,
    screen: `${screen.width}x${screen.height}`,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
  };
}
