import React, { useState, type FormEvent } from "react";



const Unauthorized: React.FC= ({  }) => {



    return (
        <>
        <div className="relative bg-white dark:bg-gray-900 py-8 px-4 flex flex-col items-center transition-colors duration-300">
                <h1>Acesso negado</h1>
                <p>Você não tem permissão para acessar esta página.</p>
                <a href="/login">
                <button
                    type="submit"
                    className="mx-auto block  max-w-xs bg-gradient-to-r from-blue-700 via-cyan-400 to-blue-600 dark:from-gray-800 dark:via-cyan-900 dark:to-gray-700 text-white font-extrabold py-3 rounded-xl shadow-lg hover:from-blue-800 hover:to-cyan-500 dark:hover:from-gray-900 dark:hover:to-cyan-800 hover:scale-105 transition-all duration-200 ease-in-out mb-5 focus:outline-none focus:ring-4 focus:ring-cyan-400/60 dark:focus:ring-cyan-900/60 focus:ring-offset-2 active:scale-95"
                
          style={{ padding: '10px 50px',  'not-allowed' : 'pointer' }}>Logar</button></a>
        </div>
        </>
    );
};

export default Unauthorized;