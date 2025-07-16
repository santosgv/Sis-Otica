import React, { useState, useEffect, useCallback } from "react";
import { ThemeContext } from "./themecontext";

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [theme, setThemeState] = useState<string>(() => {
        return localStorage.getItem("theme") || "light";
    });

    useEffect(() => {
        localStorage.setItem("theme", theme);
        document.documentElement.classList.remove("light", "dark");
        document.documentElement.classList.add(theme);
    }, [theme]);

    const toggleTheme = useCallback(() => {
        setThemeState((prev) => (prev === "dark" ? "light" : "dark"));
    }, []);

    const setTheme = useCallback((t: string) => {
        setThemeState(t === "dark" ? "dark" : "light");
    }, []);

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme, setTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};
