import React, { createContext, useContext, useState, useCallback } from "react";
import Toast from "./Toast";
import type { ToastProps } from "./Toast";

export type ToastItem = ToastProps & { id: number };

interface ToastContextType {
    showToast: (msg: string, type?: ToastProps["type"], duration?: number) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

let toastId = 0;

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [toasts, setToasts] = useState<ToastItem[]>([]);

    const showToast = useCallback((message: string, type: ToastProps["type"] = "info", duration = 3000) => {
        const id = ++toastId;
        setToasts((prev) => [...prev, { id, message, type, duration }]);
        setTimeout(() => setToasts((prev) => prev.filter((t) => t.id !== id)), duration);
    }, []);

    const handleClose = (id: number) => setToasts((prev) => prev.filter((t) => t.id !== id));

    return (
        <ToastContext.Provider value={{ showToast }}>
            {children}
            <div className="fixed top-4 right-4 z-[9999] flex flex-col gap-2 max-w-xs w-full">
                {toasts.map((toast) => (
                    <Toast key={toast.id} {...toast} onClose={() => handleClose(toast.id)} />
                ))}
            </div>
        </ToastContext.Provider>
    );
};

export function useToast() {
    const ctx = useContext(ToastContext);
    if (!ctx) throw new Error("useToast deve ser usado dentro de ToastProvider");
    return ctx;
}
