import React from "react";

export const Spinner: React.FC<{ size?: number; className?: string }> = ({ size = 24, className = "" }) => (
    <span
        className={`inline-block animate-spin border-2 border-t-transparent border-current rounded-full ${className}`}
        style={{ width: size, height: size }}
        aria-label="Carregando"
    />
);

export default Spinner;
