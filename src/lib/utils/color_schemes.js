// Theme color mapping - different shades of green
export const themeColors = {
  // Default military green for fallback
  default: "#4b5320",
  // Different greens for specific themes (examples)
  Women: "#2e8b57", // sea green
  Black: "#006400", // dark green
  Hispanic: "#228b22", // forest green
  "Asian or Pacific Islander": "#3cb371", // medium sea green
  "Native American": "#008000", // green
  "LGBTQ+": "#32cd32", // lime green
  "Generic DEI": "#6b8e23", // olive drab
  Other: "#556b2f", // dark olive green
};

// Type color mapping - different shades of green
export const typeColors = {
  // Default color for fallback
  default: "#264027",
  "Explicit heritage and DEI events": "#1d8348", // dark green
  "Everyday celebrations of heritage or ethnicity": "#117a65", // jungle green
  "Facts of history that relate to a specific ethnic group": "#0e6655", // teal
  "Mentions of personnel that highlight their ethnicity": "#148f77", // persian green
  "Military personnel that belong to a specific ethnic group, even if that isn't explicity mentioned":
    "#1abc9c", // turquoise
  Other: "#48c9b0", // medium turquoise
};

// Helper functions to get colors
export function getThemeColor(theme) {
  return themeColors[theme] || themeColors["default"];
}

export function getTypeColor(type) {
  return typeColors[type] || typeColors["default"];
}
