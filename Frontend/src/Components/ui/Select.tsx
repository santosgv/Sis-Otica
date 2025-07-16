import React from "react";

export type SelectProps = React.SelectHTMLAttributes<HTMLSelectElement> & {
    size?: "sm" | "md" | "lg";
    variant?: "primary" | "outline";
};

const base = "block w-full rounded border bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition";
const variants = {
    primary: "border-gray-300 dark:border-gray-700",
    outline: "border-2 border-blue-500 dark:border-blue-400",
};
const sizes: Record<string, string> = {
    sm: "text-xs px-2 py-1 h-8",
    md: "text-sm px-3 py-2 h-10",
    lg: "text-base px-4 py-3 h-12",
};

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
    ({ size = "md", variant = "primary", className = "", children, ...props }, ref) => (
        <select ref={ref} className={`${base} ${variants[variant] || variants.primary} ${sizes[size!] || sizes.md} ${className}`} {...props}>
            {children}
        </select>
    )
);
Select.displayName = "Select";

export default Select;
