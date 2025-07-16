import React from "react";

export type InputProps = React.InputHTMLAttributes<HTMLInputElement> & {
    size?: "sm" | "md" | "lg";
};

const base = "block w-full rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition placeholder:text-gray-400 dark:placeholder:text-gray-500";
const sizes: Record<string, string> = {
    sm: "text-xs px-2 py-1 h-8",
    md: "text-sm px-3 py-2 h-10",
    lg: "text-base px-4 py-3 h-12",
};

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ size = "md", className = "", ...props }, ref) => (
        <input ref={ref} className={`${base} ${sizes[size!] || sizes.md} ${className}`} {...props} />
    )
);
Input.displayName = "Input";

export default Input;
