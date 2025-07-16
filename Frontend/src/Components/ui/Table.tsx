import React from "react";

export type TableProps = React.TableHTMLAttributes<HTMLTableElement> & {
    variant?: "default" | "outline";
    size?: "sm" | "md" | "lg";
};

const base = "w-full border-collapse rounded shadow bg-white dark:bg-gray-800 text-gray-900 dark:text-white overflow-x-auto";
const variants = {
    default: "",
    outline: "border border-gray-300 dark:border-gray-700",
};
const sizes: Record<string, string> = {
    sm: "text-xs",
    md: "text-sm",
    lg: "text-base",
};

export const Table: React.FC<TableProps> = ({
    variant = "default",
    size = "md",
    className = "",
    children,
    ...props
}) => (
    <div className="overflow-x-auto w-full">
        <table className={`${base} ${variants[variant]} ${sizes[size]} ${className}`} {...props}>
            {children}
        </table>
    </div>
);

export default Table;
