import React from "react";

export const ThemeContext = React.createContext<{
    theme: string;
    toggleTheme?: () => void;
    setTheme?: (theme: string) => void;
}>({ theme: "dark" });
