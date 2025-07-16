import React from 'react';

interface MoneyProps {
    value: number | string;
    className?: string;
}

function formatMoney(value: number | string) {
    let num = typeof value === 'string' ? Number(String(value).replace(/[^\d.-]/g, '').replace(',', '.')) : value;
    if (isNaN(num)) num = 0;
    return num.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

const Money: React.FC<MoneyProps> = ({ value, className }) => (
    <span className={className}>{formatMoney(value)}</span>
);

export default Money;
