import React from "react";

export const Skeleton: React.FC<{ width?: string | number; height?: string | number; className?: string }> = ({ width = '100%', height = 20, className = "" }) => (
    <div
        className={`bg-gray-200 dark:bg-gray-700 animate-pulse rounded ${className}`}
        style={{ width, height }}
        aria-label="Carregando..."
    />
);

export default Skeleton;
