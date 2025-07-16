import React from "react";

export type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: "primary" | "danger" | "outline";
    size?: "sm" | "md" | "lg";
    loading?: boolean;
};

const base = "inline-flex items-center justify-center font-semibold rounded transition focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed";
const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
    danger: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
    outline: "border border-gray-300 text-gray-800 bg-white hover:bg-gray-100 focus:ring-blue-500 dark:bg-gray-900 dark:text-white dark:border-gray-700 dark:hover:bg-gray-800",
};
const sizes: Record<string, string> = {
    sm: "text-xs px-3 py-1.5 h-8",
    md: "text-sm px-4 py-2 h-10",
    lg: "text-base px-6 py-3 h-12",
};

export const Button: React.FC<ButtonProps> = ({
    variant = "primary",
    size = "md",
    loading = false,
    className = "",
    children,
    ...props
}) => (
    <button
        className={`${base} ${variants[variant] || variants.primary} ${sizes[size!] || sizes.md} ${className}`}
        disabled={loading || props.disabled}
        {...props}
    >
        {loading ? <span className="animate-spin mr-2 w-4 h-4 border-2 border-t-transparent border-current rounded-full"></span> : null}
        {children}
    </button>
);

export default Button;
