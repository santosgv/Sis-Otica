import React from "react";

export type ToastProps = {
    message: string;
    type?: "success" | "error" | "info";
    onClose?: () => void;
    duration?: number;
};

const typeStyles: Record<string, string> = {
    success: "bg-green-500 text-white",
    error: "bg-red-500 text-white",
    info: "bg-blue-500 text-white",
};

export const Toast: React.FC<ToastProps> = ({ message, type = "info", onClose, duration = 3000 }) => {
    React.useEffect(() => {
        if (!onClose) return;
        const timer = setTimeout(onClose, duration);
        return () => clearTimeout(timer);
    }, [onClose, duration]);

    return (
        <div className={`fixed top-6 right-6 z-50 px-4 py-3 rounded shadow-lg font-semibold ${typeStyles[type]}`}
            role="alert"
        >
            {message}
            {onClose && (
                <button className="ml-4 text-white/80 hover:text-white font-bold" onClick={onClose} aria-label="Fechar">×</button>
            )}
        </div>
    );
};

export default Toast;
